"""Top-level Manatal client."""

from __future__ import annotations

import os
from typing import Any, Mapping, MutableMapping, Optional

import httpx

from manatal._http import HttpTransport
from manatal._throttle import RateLimiter
from manatal.resources.candidates import CandidatesResource
from manatal.resources.contacts import ContactsResource
from manatal.resources.jobs import JobsResource
from manatal.resources.lookups import (
    CurrenciesResource,
    IndustriesResource,
    JobPipelinesResource,
    LanguagesResource,
    MatchStagesResource,
    NationalitiesResource,
    SkillsResource,
)
from manatal.resources.matches import MatchesResource
from manatal.resources.organizations import OrganizationsResource
from manatal.resources.users import UsersResource


class Manatal:
    """Synchronous client for the Manatal Open API v3.

    Example::

        from manatal import Manatal

        client = Manatal(api_key="...")
        for candidate in client.candidates.list():
            print(candidate.id)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        max_retries: int = 3,
        rate_limit: int = 90,
        rate_period: float = 60.0,
        default_page_size: int = 100,
        timeout: Optional[httpx.Timeout] = None,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        key = api_key or os.environ.get("MANATAL_API_KEY")
        if not key:
            raise ValueError(
                "api_key is required (pass api_key=... or set MANATAL_API_KEY)"
            )
        if default_page_size < 1 or default_page_size > 100:
            raise ValueError("default_page_size must be between 1 and 100")

        self.default_page_size = default_page_size
        self._limiter = RateLimiter(max_requests=rate_limit, period_seconds=rate_period)
        self._http = HttpTransport(
            key,
            timeout=timeout,
            max_retries=max_retries,
            transport=transport,
        )

        self.candidates = CandidatesResource(self)
        self.jobs = JobsResource(self)
        self.organizations = OrganizationsResource(self)
        self.matches = MatchesResource(self)
        self.contacts = ContactsResource(self)
        self.users = UsersResource(self)
        self.currencies = CurrenciesResource(self)
        self.languages = LanguagesResource(self)
        self.nationalities = NationalitiesResource(self)
        self.industries = IndustriesResource(self)
        self.job_pipelines = JobPipelinesResource(self)
        self.match_stages = MatchStagesResource(self)
        self.skills = SkillsResource(self)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Any = None,
        content: Any = None,
        headers: Optional[MutableMapping[str, str]] = None,
        files: Any = None,
    ) -> Any:
        """Send a raw request against the Open API."""
        return self._http.request(
            method,
            path,
            params=params,
            json=json,
            content=content,
            headers=headers,
            files=files,
            acquire=self._limiter.acquire,
        )

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "Manatal":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
