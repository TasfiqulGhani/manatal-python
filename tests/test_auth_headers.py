import httpx
import respx

from manatal import Manatal
from manatal._http import DEFAULT_BASE_URL


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
    assert route.calls[0].request.headers["Authorization"] == "Token secret-token"
    assert "manatal-python/" in route.calls[0].request.headers["User-Agent"]
    client.close()


def test_api_key_from_env(monkeypatch):
    monkeypatch.setenv("MANATAL_API_KEY", "env-key")
    client = Manatal(rate_limit=1000)
    assert client._http.api_key == "env-key"
    client.close()
