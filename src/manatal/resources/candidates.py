"""Candidates and nested candidate resources."""

from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from manatal._base import NestedResource, PathId, Resource

if TYPE_CHECKING:
    from manatal._client import Manatal


class CandidatesResource(Resource):
    path = "/candidates/"

    def activities(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "activities")

    def attachments(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "attachments")

    def educations(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "educations")

    def experiences(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "experiences")

    def matches(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "matches")

    def nationalities(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "nationalities")

    def notes(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "notes")

    def social_media(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "social-media")

    def skills(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "skills")

    def tags(self, candidate_id: PathId) -> NestedResource:
        return NestedResource(self._client, self.path, candidate_id, "tags")

    def resume(self, candidate_id: PathId) -> "CandidateResumeResource":
        return CandidateResumeResource(self._client, candidate_id)

    def create_skills_bulk(
        self, candidate_id: PathId, skills: list
    ) -> Dict[str, Any]:
        """Bulk-create skills for a candidate."""
        path = f"{self._collection()}{candidate_id}/skills/bulk/"
        return self._client.request("POST", path, json={"skills": skills})


class CandidateResumeResource:
    def __init__(self, client: "Manatal", candidate_id: PathId) -> None:
        self._client = client
        self._base = f"/candidates/{candidate_id}/resume/"

    def list(self) -> Any:
        return self._client.request("GET", self._base)

    def create(self, *, file_name: str, file_content: bytes, content_type: str = "application/octet-stream") -> Any:
        files = {"file": (file_name, file_content, content_type)}
        return self._client.request("POST", self._base, files=files)

    def delete(self, id: PathId) -> None:
        self._client.request("DELETE", f"{self._base}{id}/")
