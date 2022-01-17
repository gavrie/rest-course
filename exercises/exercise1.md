# Exercise 1

Based on the code from the `master` branch:

1. Implement the `DELETE` method for a single BDB
  - Question: Should the delete method return any data to the client? Why? Which HTTP status code should be used?
  - Note: In case you decide that nothing should be returned, note that there is no way to say so in Python (like you could do with e.g. `void` in other languages). The default in Python is to return `None`, which FastAPI will convert to the JSON value `null`. To tell FastAPI that you really do not want to return any data to the client, use the following:

    `return Response(status_code=HTTP_204_NO_CONTENT)`

2. Use the delete method in the test code to clean up any resources created by the test: Each test should clean up after itself, and the test suite should clean up resources created by the fixture ([use `yield` in the `setup` function](https://docs.pytest.org/en/6.2.x/fixture.html#teardown-cleanup-aka-fixture-finalization))
3. Implement bulk `DELETE` for all BDBs
  - What should the endpoint for this be?