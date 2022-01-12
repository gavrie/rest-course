import random

import httpx
import pytest

BASE_URL = "http://localhost:8000"
BDBS_URL = f"{BASE_URL}/bdbs"
EVENTS_URL = f"{BASE_URL}/test/events"


@pytest.fixture(scope="module")
def client():
    return httpx.Client(
        timeout=3600,
        event_hooks={"response": [lambda r: r.raise_for_status()]},
    )


@pytest.fixture(scope="module", autouse=True)
def setup(client):
    # Create some BDBs
    for _ in range(5):
        i = random.randint(1000, 10000)
        params = {"name": f"foo{i}", "memory_size": i}
        client.post(BDBS_URL, json=params)


def test_create_bdb(client):
    """
    Assumptions:
     - We do not rely on any preexisting server-side objects
     - Other requests may create and modify such objects while we run
     - Objects created by us belong to us, others should not touch them
    """

    # Get current list of BDBs
    r = client.get(BDBS_URL)
    bdb_responses = r.json()
    bdb_uids_before = set(bdb_response["bdb"]["uid"] for bdb_response in bdb_responses)

    # Create a BDB
    params = {"name": "foo", "memory_size": 2}
    r = client.post(BDBS_URL, json=params)
    bdb_response = r.json()
    bdb = bdb_response["bdb"]
    url = bdb_response["url"]

    assert bdb["uid"] is not None
    assert bdb["name"] == params["name"]
    assert bdb["memory_size"] == params["memory_size"]

    uid = bdb["uid"]
    assert uid not in bdb_uids_before, "UID was unexpectedly reused"

    # Get the BDB
    location = r.headers["location"]
    assert url == location

    r = client.get(url)
    bdb_response = r.json()

    assert bdb_response["bdb"] == bdb, "BDB has changed since creation"

    # Check that new BDB is in list
    r = client.get(BDBS_URL)
    bdb_responses = r.json()
    bdb_uids = set(bdb_response["bdb"]["uid"] for bdb_response in bdb_responses)

    assert uid in bdb_uids

    # Clean up
    # TODO: Not implemented yet on the server side
    # client.delete(bdb_url)


def test_updating_with_bad_params_fails(client):
    # Create a BDB
    params = {"name": "foo", "memory_size": 2}
    r = client.post(BDBS_URL, json=params)
    bdb_response = r.json()
    bdb = bdb_response["bdb"]
    bdb_url = bdb_response["url"]

    # Update the BDB
    bdb["memory_size"] = 1

    with pytest.raises(httpx.HTTPStatusError, match="422"):
        client.put(bdb_url, json=bdb)


def test_updating_after_conflicting_update_fails(client):
    # Create a BDB
    params = {"name": "foo", "memory_size": 2}
    r = client.post(BDBS_URL, json=params)
    bdb_response = r.json()
    bdb = bdb_response["bdb"]
    bdb_url = bdb_response["url"]
    print(f"\n*** BDB: {bdb=}")

    # Wait for conflicting update to happen
    event = client.post(EVENTS_URL).json()
    print(f"\n*** Waiting for event: {event=}")
    print(f"\nUpdate the BDB with a memory_size of 8 and then trigger the event.")
    client.get(event["url"])

    # Update the BDB
    bdb["memory_size"] = 4  # Will fail if updated to a larger size in the meantime
    client.put(bdb_url, json=bdb)

    with pytest.raises(httpx.HTTPStatusError, match="409"):
        client.put(bdb_url, json=bdb)


def test_lost_updates_are_avoided(client):
    # Create a BDB
    r = client.post(BDBS_URL, json={"name": "foo", "memory_size": 2})
    j = r.json()

    bdb, bdb_url = j["bdb"], j["url"]
    etag = r.headers["etag"]

    # Updating the BDB without etag fails
    with pytest.raises(httpx.HTTPStatusError, match="428"):
        client.put(bdb_url, json=bdb)

    # Updating the BDB with correct etag succeeds
    client.put(bdb_url, headers={"if-match": etag}, json=bdb)

    # Updating the BDB with wrong etag fails
    with pytest.raises(httpx.HTTPStatusError, match="412"):
        client.put(bdb_url, headers={"if-match": '"no-such-etag"'}, json=bdb)

    # Updating the BDB with different content invalidates the old etag
    bdb["name"] = "bar"
    client.put(bdb_url, headers={"if-match": etag}, json=bdb)
    with pytest.raises(httpx.HTTPStatusError, match="412"):
        client.put(bdb_url, headers={"if-match": etag}, json=bdb)
