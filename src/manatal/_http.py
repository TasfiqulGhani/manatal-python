"""HTTP transport with retries for Manatal Open API."""

from __future__ import annotations

import time
from typing import Any, Callable, Mapping, MutableMapping, Optional

import httpx

from manatal._headers import build_sdk_headers
from manatal.models import wrap
from manatal.exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ForbiddenError,
    RateLimitError,
    ValidationError,
)

DEFAULT_BASE_URL = "https://api.manatal.com/open/v3"
DEFAULT_TIMEOUT = httpx.Timeout(30.0, connect=10.0)
TRANSIENT_STATUS = frozenset({502, 503, 504})
IDEMPOTENT_METHODS = frozenset({"GET", "HEAD", "OPTIONS", "DELETE"})


def _parse_retry_after(headers: Mapping[str, str]) -> Optional[float]:
    value = headers.get("Retry-After") or headers.get("retry-after")
    if value is None:
        return None
    try:
        return max(0.0, float(value))
    except (TypeError, ValueError):
        return None


def raise_for_status(
    response: httpx.Response,
    *,
    retry_after: Optional[float] = None,
) -> None:
    """Map HTTP errors to typed Manatal exceptions."""
    if response.is_success:
        return

    try:
        body: Any = response.json()
    except Exception:
        body = response.text

    detail = None
    if isinstance(body, dict):
        detail = body.get("detail") or body
    message = (
        detail
        if isinstance(detail, str)
        else f"HTTP {response.status_code} error"
    )
    headers = dict(response.headers)
    status = response.status_code

    if status == 401:
        raise AuthenticationError(
            str(message), status_code=status, body=body, headers=headers
        )
    if status == 403:
        raise ForbiddenError(
            str(message), status_code=status, body=body, headers=headers
        )
    if status == 404:
        raise NotFoundError(
            str(message), status_code=status, body=body, headers=headers
        )
    if status == 400:
        raise ValidationError(
            str(message) if isinstance(detail, str) else "Validation error",
            status_code=status,
            body=body,
            headers=headers,
        )
    if status == 429:
        raise RateLimitError(
            str(message),
            status_code=status,
            body=body,
            headers=headers,
            retry_after=retry_after or _parse_retry_after(headers),
        )
    raise APIError(str(message), status_code=status, body=body, headers=headers)


class HttpTransport:
    """HTTP client with retries for temporary errors."""

    def __init__(
        self,
        api_key: str,
        *,
        timeout: Optional[httpx.Timeout] = None,
        max_retries: int = 3,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        self.api_key = api_key
        self.max_retries = max_retries
        self._client = httpx.Client(
            base_url=DEFAULT_BASE_URL,
            timeout=timeout or DEFAULT_TIMEOUT,
            headers=build_sdk_headers(api_key),
            transport=transport,
            follow_redirects=True,
        )

    def close(self) -> None:
        self._client.close()

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Any = None,
        content: Any = None,
        headers: Optional[MutableMapping[str, str]] = None,
        files: Any = None,
        acquire: Optional[Callable[[], None]] = None,
    ) -> Any:
        method_upper = method.upper()
        attempt = 0
        while True:
            if acquire is not None:
                acquire()

            response = self._client.request(
                method_upper,
                url,
                params=params,
                json=json,
                content=content,
                headers=headers,
                files=files,
            )

            if self._should_retry(method_upper, response.status_code, attempt):
                wait = _parse_retry_after(response.headers)
                if wait is None:
                    wait = min(float(2**attempt), 30.0)
                attempt += 1
                if attempt > self.max_retries:
                    raise_for_status(response, retry_after=wait)
                time.sleep(wait)
                continue

            if response.status_code == 204:
                return None

            raise_for_status(response)

            if not response.content:
                return None
            content_type = response.headers.get("content-type", "")
            if "application/json" in content_type:
                return wrap(response.json())
            return response.content

    def _should_retry(self, method: str, status: int, attempt: int) -> bool:
        if attempt >= self.max_retries:
            return False
        if status == 429:
            return True
        if status in TRANSIENT_STATUS and method in IDEMPOTENT_METHODS:
            return True
        return False
