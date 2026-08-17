"""Lookup / reference data resources."""

from __future__ import annotations

from typing import Any, Dict, List

from manatal._base import PathId, ReadOnlyResource, Resource


class CurrenciesResource(ReadOnlyResource):
    path = "/currencies/"


class LanguagesResource(ReadOnlyResource):
    path = "/languages/"


class NationalitiesResource(ReadOnlyResource):
    path = "/nationalities/"


class IndustriesResource(ReadOnlyResource):
    path = "/industries/"


class JobPipelinesResource(ReadOnlyResource):
    path = "/job-pipelines/"


class MatchStagesResource(ReadOnlyResource):
    path = "/match-stages/"


class SkillsResource(Resource):
    """Client skills catalog (`/skills/`)."""

    path = "/skills/"

    def create(self, **data: Any) -> Dict[str, Any]:
        """Bulk create client skills."""
        return self._client.request("POST", self._collection(), json=data)

    def create_names(self, names: List[str]) -> Dict[str, Any]:
        return self.create(names=names)

    def retrieve(self, id: PathId) -> Dict[str, Any]:
        raise NotImplementedError("/skills/ does not support retrieve")

    def update(self, id: PathId, **data: Any) -> Dict[str, Any]:
        raise NotImplementedError("/skills/ does not support update")

    def delete(self, id: PathId) -> None:
        raise NotImplementedError("/skills/ does not support delete")
