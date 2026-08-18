import httpx
import respx

from manatal import Manatal
from manatal._headers import SDK_LANGUAGE, SDK_NAME
from manatal._http import DEFAULT_BASE_URL
from manatal._version import __version__


@respx.mock
def test_authorization_token_header():
    route = respx.get(f"{DEFAULT_BASE_URL}/candidates/").mock(
        return_value=httpx.Response(
            200,
            json={"count": 0, "next": None, "previous": None, "results": []},
        )
    )
    client = Manatal(api_key="secret-token", rate_limit=1000)
    list(client.candidates.list())
    assert route.called
    headers = route.calls[0].request.headers
    assert headers["Authorization"] == "Token secret-token"
    assert headers["User-Agent"] == f"{SDK_NAME}/{__version__}"
    assert headers["X-Manatal-SDK"] == SDK_NAME
    assert headers["X-Manatal-SDK-Version"] == __version__
    assert headers["X-Manatal-SDK-Language"] == SDK_LANGUAGE
    client.close()


def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv("MANATAL_API_KEY", "env-key")
    client = Manatal(rate_limit=1000)
    assert client._http.api_key == "env-key"
    client.close()
