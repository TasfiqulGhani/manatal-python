"""Pagination helpers for DRF page-number responses."""

from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, TYPE_CHECKING

from manatal.models import ManatalObject, wrap

if TYPE_CHECKING:
    from manatal._client import Manatal


class Page:
    """Single page of list results."""

    def __init__(self, data: Dict[str, Any]) -> None:
        self.count: int = int(data.get("count") or 0)
        self.next: Optional[str] = data.get("next")
        self.previous: Optional[str] = data.get("previous")
        self.results: List[ManatalObject] = [
            wrap(item) for item in (data.get("results") or [])
        ]

    def __iter__(self) -> Iterator[ManatalObject]:
        return iter(self.results)

    def __len__(self) -> int:
        return len(self.results)


def iter_pages(
    client: "Manatal",
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
) -> Iterator[Page]:
    """Yield successive pages, following absolute ``next`` URLs from the API."""
    query = dict(params or {})
    if "page_size" not in query:
        query["page_size"] = client.default_page_size

    data = client.request("GET", path, params=query)
    page = Page(data)
    yield page

    while page.next:
        data = client.request("GET", page.next)
        page = Page(data)
        yield page


def iter_results(
    client: "Manatal",
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
) -> Iterator[ManatalObject]:
    """Yield every item across all pages."""
    for page in iter_pages(client, path, params=params):
        yield from page.results
