"""Matches and nested match resources."""

from __future__ import annotations

from manatal._base import NestedResource, PathId, Resource


class MatchesResource(Resource):
    path = "/matches/"

    def activities(self, match_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, match_id, "activities")

    def attachments(self, match_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, match_id, "attachments")

    def notes(self, match_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, match_id, "notes")
