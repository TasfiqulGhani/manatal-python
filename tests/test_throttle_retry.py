import httpx
import respx

from manatal import Manatal, RateLimitError
from manatal._http import DEFAULT_BASE_URL
from manatal._throttle import RateLimiter


@respx.mock
def test_retries_on_429_with_retry_after(monkeypatch):
    monkeypatch.setattr("manatal._http.time.sleep", lambda _: None)
    route = respx.get(f"{DEFAULT_BASE_URL}/candidates/1/").mock(
        side_effect=[
            httpx.Response(
                429,
                json={"detail": "Request was throttled. Expected available in 1 seconds."},
                headers={"Retry-After": "1"},
            ),
            httpx.Response(200, json={"id": 1, "full_name": "Ada"}),
        ]
    )
    client = Manatal(api_key="k", rate_limit=1000, max_retries=3)
    data = client.candidates.retrieve(1)
    assert data["id"] == 1
    assert route.call_count == 2
    client.close()


@respx.mock
def test_rate_limit_exhausted(monkeypatch):
    monkeypatch.setattr("manatal._http.time.sleep", lambda _: None)
    respx.get(f"{DEFAULT_BASE_URL}/candidates/1/").mock(
        return_value=httpx.Response(
            429,
            json={"detail": "throttled"},
            headers={"Retry-After": "1"},
        )
    )
    client = Manatal(api_key="k", rate_limit=1000, max_retries=2)
    try:
        client.candidates.retrieve(1)
        assert False, "expected RateLimitError"
    except RateLimitError as exc:
        assert exc.status_code == 429
        assert exc.retry_after == 1.0
    finally:
        client.close()


def test_rate_limiter_allows_under_cap():
    limiter = RateLimiter(max_requests=3, period_seconds=60.0)
    limiter.acquire()
    limiter.acquire()
    limiter.acquire()
    assert len(limiter._timestamps) == 3
