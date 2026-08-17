"""Shared resource helpers."""

from __future__ import annotations

from typing import Any, Dict, Iterator, Optional, TYPE_CHECKING, Union

from manatal.models import ManatalObject

from manatal._pagination import Page, iter_pages, iter_results

if TYPE_CHECKING:
    from manatal._client import Manatal

PathId = Union[int, str]


class Resource:
    """Base CRUD resource against a collection path."""

    path: str = ""

    def __init__(self, client: "Manatal") -> None:
        self._client = client

    def _collection(self) -> str:
        return self.path if self.path.endswith("/") else f"{self.path}/"

    def _item(self, id: PathId) -> str:
        return f"{self._collection()}{id}/"

    def list_page(
        self,
        *,
        page: int = 1,
        page_size: Optional[int] = None,
        **filters: Any,
    ) -> Page:
        params: Dict[str, Any] = {"page": page, **filters}
        params["page_size"] = (
            page_size if page_size is not None else self._client.default_page_size
        )
        data = self._client.request("GET", self._collection(), params=params)
        return Page(data)

    def list(self, **filters: Any) -> Iterator[ManatalObject]:
        return iter_results(self._client, self._collection(), params=filters)

    def list_pages(self, **filters: Any) -> Iterator[Page]:
        return iter_pages(self._client, self._collection(), params=filters)

    def retrieve(self, id: PathId) -> ManatalObject:
        return self._client.request("GET", self._item(id))

    def create(self, **data: Any) -> ManatalObject:
        return self._client.request("POST", self._collection(), json=data)

    def update(self, id: PathId, **data: Any) -> ManatalObject:
        return self._client.request("PATCH", self._item(id), json=data)

    def delete(self, id: PathId) -> None:
        self._client.request("DELETE", self._item(id))


class NestedResource:
    """Nested collection under a parent object, e.g. /candidates/{pk}/notes/."""

    def __init__(
        self,
        client: "Manatal",
        parent_path: str,
        parent_id: PathId,
        nested: str,
    ) -> None:
        self._client = client
        base = parent_path if parent_path.endswith("/") else f"{parent_path}/"
        self._base = f"{base}{parent_id}/{nested.strip('/')}/"

    def _item(self, id: PathId) -> str:
        return f"{self._base}{id}/"

    def list_page(
        self,
        *,
        page: int = 1,
        page_size: Optional[int] = None,
        **filters: Any,
    ) -> Page:
        params: Dict[str, Any] = {"page": page, **filters}
        params["page_size"] = (
            page_size if page_size is not None else self._client.default_page_size
        )
        data = self._client.request("GET", self._base, params=params)
        return Page(data)

    def list(self, **filters: Any) -> Iterator[ManatalObject]:
        return iter_results(self._client, self._base, params=filters)

    def retrieve(self, id: PathId) -> ManatalObject:
        return self._client.request("GET", self._item(id))

    def create(self, **data: Any) -> ManatalObject:
        return self._client.request("POST", self._base, json=data)

    def update(self, id: PathId, **data: Any) -> ManatalObject:
        return self._client.request("PATCH", self._item(id), json=data)

    def delete(self, id: PathId) -> None:
        self._client.request("DELETE", self._item(id))


class ReadOnlyResource(Resource):
    """Resource that only supports list/retrieve."""

    def create(self, **data: Any) -> ManatalObject:
        raise NotImplementedError(f"{self.path} does not support create")

    def update(self, id: PathId, **data: Any) -> ManatalObject:
        raise NotImplementedError(f"{self.path} does not support update")

    def delete(self, id: PathId) -> None:
        raise NotImplementedError(f"{self.path} does not support delete")
