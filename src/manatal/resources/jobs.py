"""Jobs and nested job resources."""

from __future__ import annotations

from manatal._base import NestedResource, PathId, Resource


class JobsResource(Resource):
    path = "/jobs/"

    def activities(self, job_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, job_id, "activities")

    def attachments(self, job_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, job_id, "attachments")

    def matches(self, job_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, job_id, "matches")

    def notes(self, job_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, job_id, "notes")
