import httpx
import respx

from manatal import Manatal
from manatal._http import DEFAULT_BASE_URL


@respx.mock
def test_list_follows_next():
    def _handler(request: httpx.Request) -> httpx.Response:
        page = request.url.params.get("page", "1")
        if page == "2":
            return httpx.Response(
                200,
                json={
                    "count": 2,
                    "next": None,
                    "previous": f"{DEFAULT_BASE_URL}/candidates/?page=1&page_size=100",
                    "results": [{"id": 2}],
                },
            )
        return httpx.Response(
            200,
            json={
                "count": 2,
                "next": f"{DEFAULT_BASE_URL}/candidates/?page=2&page_size=100",
                "previous": None,
                "results": [{"id": 1}],
            },
        )

    respx.get(url__regex=r".*/candidates/.*").mock(side_effect=_handler)
    client = Manatal(api_key="k", rate_limit=1000)
    ids = [c.id for c in client.candidates.list()]
    assert ids == [1, 2]
    client.close()


@respx.mock
def test_list_page_single():
    respx.get(url__regex=r".*/jobs/.*").mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 1,
                "next": None,
                "previous": None,
                "results": [{"id": 9}],
            },
        )
    )
    client = Manatal(api_key="k", rate_limit=1000)
    page = client.jobs.list_page(page=1, page_size=10)
    assert page.count == 1
    assert page.results[0].id == 9
    client.close()
