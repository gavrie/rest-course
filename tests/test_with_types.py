import random
from dataclasses import asdict

import httpx
import pytest

from rest_course.params import BDBParams
from rest_course.types import BDB, UID

BASE_URL = "http://localhost:8000"
BDBS_URL = f"{BASE_URL}/bdbs"


@pytest.fixture(scope="module")
def client():
    return httpx.Client(event_hooks={"response": [lambda r: r.raise_for_status()]})


@pytest.fixture(scope="module", autouse=True)
def setup(client):
    # Create some BDBs
    for _ in range(5):
        i = random.randint(1000, 10000)
        params = BDBParams(name=f"foo{i}", memory_size=i)
        client.post(BDBS_URL, json=asdict(params))


def test_create_bdb(client):
    """
    Assumptions:
     - We do not rely on any preexisting server-side objects
     - Other requests may create and modify such objects while we run
     - Objects created by us belong to us, others should not touch them
    """

    # Get current list of BDBs
    r = client.get(BDBS_URL)
    bdb_uids_before = set(UID(bdb["uid"]) for bdb in r.json())

    # Create a BDB
    params = BDBParams(name=f"foo", memory_size=2)
    r = client.post(BDBS_URL, json=asdict(params))
    bdb = BDB(**r.json())

    assert bdb.name == params.name
    assert bdb.memory_size == params.memory_size

    uid = bdb.uid
    assert uid not in bdb_uids_before, "UID was unexpectedly reused"

    # Get the BDB
    bdb_url = f"{BDBS_URL}/{uid}"  # Ugly: manual composition of URL
    r = client.get(bdb_url)
    assert BDB(**r.json()) == bdb, "BDB has changed since creation"

    # Check that new BDB is in list
    r = client.get(BDBS_URL)
    bdb_uids = set(UID(bdb["uid"]) for bdb in r.json())

    assert uid in bdb_uids

    # Clean up
    # TODO: Not implemented yet on the server side
    # client.delete(bdb_url)
