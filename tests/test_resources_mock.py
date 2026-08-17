import httpx
import respx

from manatal import Manatal, NotFoundError, ValidationError
from manatal._http import DEFAULT_BASE_URL


@respx.mock
def test_create_and_update_use_post_and_patch():
    create = respx.post(f"{DEFAULT_BASE_URL}/candidates/").mock(
        return_value=httpx.Response(201, json={"id": 5, "full_name": "A"})
    )
    update = respx.patch(f"{DEFAULT_BASE_URL}/candidates/5/").mock(
        return_value=httpx.Response(200, json={"id": 5, "full_name": "B"})
    )
    client = Manatal(api_key="k", rate_limit=1000)
    created = client.candidates.create(full_name="A")
    updated = client.candidates.update(5, full_name="B")
    assert created.id == 5
    assert created["id"] == 5
    assert updated.full_name == "B"
    assert create.called and update.called
    client.close()


@respx.mock
def test_nested_notes():
    respx.post(f"{DEFAULT_BASE_URL}/candidates/3/notes/").mock(
        return_value=httpx.Response(201, json={"id": 1, "info": "hi"})
    )
    client = Manatal(api_key="k", rate_limit=1000)
    note = client.candidates.notes(3).create(info="hi")
    assert note["info"] == "hi"
    client.close()


@respx.mock
def test_not_found_and_validation():
    respx.get(f"{DEFAULT_BASE_URL}/jobs/404/").mock(
        return_value=httpx.Response(404, json={"detail": "Not found."})
    )
    respx.post(f"{DEFAULT_BASE_URL}/jobs/").mock(
        return_value=httpx.Response(400, json={"position_name": ["This field is required."]})
    )
    client = Manatal(api_key="k", rate_limit=1000)
    try:
        client.jobs.retrieve(404)
        assert False
    except NotFoundError:
        pass
    try:
        client.jobs.create()
        assert False
    except ValidationError as exc:
        assert exc.status_code == 400
    client.close()
