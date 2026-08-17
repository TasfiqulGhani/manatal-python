"""Contacts and nested contact resources."""

from __future__ import annotations

from manatal._base import NestedResource, PathId, Resource


class ContactsResource(Resource):
    path = "/contacts/"

    def activities(self, contact_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, contact_id, "activities")

    def attachments(self, contact_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, contact_id, "attachments")

    def notes(self, contact_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, contact_id, "notes")
