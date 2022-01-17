## Exercise 3.1

Branch: `lesson_082_update`

- Create an API for a upgrading a BDB to a new version specified by the user:
  - Called with `PUT /bdbs/<uid>/upgrade?version=x`
  - Question: Why is `PUT` appropriate here and not `POST`?
- The operation is long-running and normally should take around 30 seconds to complete (simulate this with `sleep` on the server side)
- While upgrading a BDB, the server should be free for other operations -- so make sure to use `async` with `anyio.sleep` instead of `time.sleep`! (see anyio basics; anyio is included with FastAPI. For a more gentle introduction, see here)
- The client will be blocked (held waiting by the server) on the `PUT` until the operation is complete
- Testing:
  - Write a test that starts an upgrade and waits for it to complete
  - Upgrade several BDBs in parallel and ensure that the total time to complete the test is not more than the required ~30 seconds (assume that the server is strong enough to run several upgrades at the same time)


## Exercise 3.2

- Implement the above upgrade API in a non-blocking way:
  - The server should immediately return a handle (`uuid` based, similar to what we did with the events).
  - The client should periodically poll the status via `GET` requests, to which the server will respond with the current progress (on a scale of 0-100% complete).
  - The client will `print` the progress to the screen (make sure to run `pytest` with the `-s` parameter to see the output in real time)
