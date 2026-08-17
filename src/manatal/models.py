"""API response objects with attribute and dict access."""

from __future__ import annotations

from typing import Any, Mapping


class ManatalObject(dict):
    """JSON object that supports both ``job.id`` and ``job["id"]``.

    Nested dicts and lists are wrapped the same way, so
    ``job.organization.name`` works when the API returns nested objects.
    Keys that are not valid Python identifiers still work with ``[]``.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__()
        data = dict(*args, **kwargs)
        for key, value in data.items():
            dict.__setitem__(self, key, wrap(value))

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as exc:
            raise AttributeError(
                f"{type(self).__name__!r} has no attribute {name!r}"
            ) from exc

    def __setattr__(self, name: str, value: Any) -> None:
        self[name] = value

    def __delattr__(self, name: str) -> None:
        try:
            del self[name]
        except KeyError as exc:
            raise AttributeError(
                f"{type(self).__name__!r} has no attribute {name!r}"
            ) from exc

    def __setitem__(self, key: Any, value: Any) -> None:
        super().__setitem__(key, wrap(value))

    def __repr__(self) -> str:
        return f"ManatalObject({super().__repr__()})"


def wrap(value: Any) -> Any:
    """Recursively wrap dicts as :class:`ManatalObject`."""
    if isinstance(value, ManatalObject):
        return value
    if isinstance(value, Mapping):
        return ManatalObject(value)
    if isinstance(value, list):
        return [wrap(item) for item in value]
    return value
