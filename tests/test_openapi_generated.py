import random

import pytest

from rest_course_client.api.bdb import create_bdb, get_all_bdbs, get_bdb
from rest_course_client.models import BDB, BDBParams

BASE_URL = "http://localhost:8000"
BDBS_URL = f"{BASE_URL}/bdbs"


@pytest.fixture(scope="module")
def client():
    """
    Client generated with:

    openapi-python-client generate --meta none --url http://localhost:8000/openapi.json
    """
    from rest_course_client import Client

    return Client(base_url=BASE_URL)


@pytest.fixture(scope="module", autouse=True)
def setup(client):
    # Create some BDBs
    for _ in range(5):
        i = random.randint(1000, 10000)
        params = BDBParams(name=f"foo{i}", memory_size=i)
        create_bdb.sync(client=client, json_body=params)


def test_create_bdb(client):
    """
    Assumptions:
     - We do not rely on any preexisting server-side objects
     - Other requests may create and modify such objects while we run
     - Objects created by us belong to us, others should not touch them
    """

    # Get current list of BDBs
    bdb_uids_before = set(bdb.uid for bdb in get_all_bdbs.sync(client=client))

    # Create a BDB
    params = BDBParams(name=f"foo", memory_size=2)
    bdb: BDB = create_bdb.sync(client=client, json_body=params)

    assert bdb.name == params.name
    assert bdb.memory_size == params.memory_size

    uid = bdb.uid
    assert uid not in bdb_uids_before, "UID was unexpectedly reused"

    # Get the BDB
    bdb_current: BDB = get_bdb.sync(uid, client=client)
    assert bdb_current == bdb, "BDB has changed since creation"

    # Check that new BDB is in list
    bdb_uids = set(bdb.uid for bdb in get_all_bdbs.sync(client=client))

    assert uid in bdb_uids

    # Clean up
    # TODO: Not implemented yet on the server side
    # client.delete(bdb_url)
