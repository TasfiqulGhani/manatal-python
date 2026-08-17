from manatal.models import ManatalObject, wrap


def test_attribute_and_dict_access():
    job = wrap({"id": 42, "position_name": "pyp", "organization": {"id": 1, "name": "Acme"}})
    assert isinstance(job, ManatalObject)
    assert job.id == 42
    assert job["id"] == 42
    assert job.position_name == "pyp"
    assert job.organization.name == "Acme"
    assert job.organization["id"] == 1


def test_missing_attribute_raises():
    job = wrap({"id": 1})
    try:
        _ = job.missing
        assert False
    except AttributeError:
        pass
