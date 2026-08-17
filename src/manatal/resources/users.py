"""Users (read-only)."""

from __future__ import annotations

from manatal._base import ReadOnlyResource


class UsersResource(ReadOnlyResource):
    path = "/users/"
