"""Exception types raised by the Manatal client."""

from __future__ import annotations

from typing import Any, Optional


class ManatalError(Exception):
    """Base error for all Manatal client failures."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        body: Any = None,
        headers: Optional[dict] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.body = body
        self.headers = headers or {}


class AuthenticationError(ManatalError):
    """Raised on 401 Unauthorized."""


class ForbiddenError(ManatalError):
    """Raised on 403 Forbidden (scope / IP whitelist)."""


class NotFoundError(ManatalError):
    """Raised on 404 Not Found."""


class ValidationError(ManatalError):
    """Raised on 400 Bad Request / validation errors."""


class RateLimitError(ManatalError):
    """Raised when the API asks the client to slow down."""

    def __init__(
        self,
        message: str,
        *,
        status_code: Optional[int] = None,
        body: Any = None,
        headers: Optional[dict] = None,
        retry_after: Optional[float] = None,
    ) -> None:
        super().__init__(
            message, status_code=status_code, body=body, headers=headers
        )
        self.retry_after = retry_after


class APIError(ManatalError):
    """Raised for other unexpected HTTP error responses."""
