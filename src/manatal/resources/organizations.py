"""Organizations and nested organization resources."""

from __future__ import annotations

from manatal._base import NestedResource, PathId, Resource


class OrganizationsResource(Resource):
    path = "/organizations/"

    def activities(self, organization_id: PathId) -> NestedResource:
        return NestedResource(
            self._client, self.path, organization_id, "activities"
        )

    def attachments(self, organization_id: PathId) -> NestedResource:
        return NestedResource(
            self._client, self.path, organization_id, "attachments"
        )

    def notes(self, organization_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, organization_id, "notes")
