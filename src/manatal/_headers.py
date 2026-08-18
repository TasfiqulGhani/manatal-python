"""Default HTTP headers sent with every Open API request."""

from __future__ import annotations

from manatal._version import __version__

SDK_NAME = "manatal-python"
SDK_LANGUAGE = "python"


def build_sdk_headers(api_key: str) -> dict[str, str]:
    """Headers attached to every SDK request for server-side analytics."""
    return {
        "Authorization": f"Token {api_key}",
        "Accept": "application/json",
        "User-Agent": f"{SDK_NAME}/{__version__}",
        "X-Manatal-SDK": SDK_NAME,
        "X-Manatal-SDK-Version": __version__,
        "X-Manatal-SDK-Language": SDK_LANGUAGE,
    }
