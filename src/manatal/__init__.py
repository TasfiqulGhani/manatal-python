"""Python SDK for the Manatal Open API."""

from manatal._client import Manatal
from manatal._version import __version__
from manatal.models import ManatalObject
from manatal.exceptions import (
    APIError,
    AuthenticationError,
    ManatalError,
    NotFoundError,
    ForbiddenError,
    RateLimitError,
    ValidationError,
)

__all__ = [
    "Manatal",
    "ManatalObject",
    "__version__",
    "ManatalError",
    "AuthenticationError",
    "ForbiddenError",
    "NotFoundError",
    "ValidationError",
    "RateLimitError",
    "APIError",
]
