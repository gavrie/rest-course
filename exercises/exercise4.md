## Exercise 4: Conditional Requests

Branch: `lesson_082_update` (same as earlier)

- Modify the app to avoid lost updates using the method we outlined (called _optimistic locking_):
  - Modify `get_bdb` to calculate and return an ETag for the BDB
  - Modify `update_bdb` to verify that the ETag specified by the client in the `If-Match` header matches the current ETag of the BDB
  - Question: What should happen is the client did not specify an `If-Match` header? Should the update suceed or not?
- Hint: You can use Python’s `hashlib` (in the standard library) to calculate hashes

Background material:

    https://httpbin.org

    # Etag:
    httpx https://httpbin.org/etag/foobar

    # If-Match:
    httpx https://httpbin.org/etag/foobar -h if-match foobar

    # If-None-Match:
    httpx https://httpbin.org/etag/foobar -h if-none-match foobar

A full description of the headers and their semantics:
https://developer.mozilla.org/en-US/docs/Web/HTTP/Conditional_requests
