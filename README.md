## Preparing for development

1. Make sure you have Python 3.9 or higher installed (it's best to use [pyenv](https://github.com/pyenv/pyenv#installation) for that, but you can use your system's Python 3.9 if you have to).
2. Install [Poetry](https://python-poetry.org/docs/#installation) to manage dependencies.
3. Have Poetry install the project's dependencies (this will create a new `virtualenv` automatically):

       poetry install


## Running

    uvicorn main:app --reload


## Testing via the API

Creating a BDB:

    $ httpx http://localhost:8000/bdbs -j '{"name":"foo","memory_size":2}'

Listing the BDBs:

    $ httpx http://localhost:8000/bdbs


## Design Concepts

- Use well-defined data types (not `dict`s!) to enable enforcing and validating correctness
- Maintain clean, separate layers for API, business logic and persistence
- Do not mix data classes ("DTOs") used in the API with those used in persistence, even though they may seem similar
- Explicitly map selected exceptions to app-level errors, to distinguish between user-caused errors and internal errors (and bugs)

## Implementation Details

- Use type annotations for code correctness and schema generation
- Generate the schema from the code and not the other way around.
  - It's much easier to maintain code than to maintain schema files.
  - If you must, store the generated schema and diff it to ensure changes are correct.
- Use generators and iterators instead of creating temporary data sets
- Use cursors (`SCAN` in Redis) to iterate external data sets

## REST Principles

- Nouns and Verbs
  - Standard verbs aren't always suitable
  - No need to follow religiously, just when it makes sense (e.g. CRUD)
  - REST vs Non-REST (RPC style). _Affordances_
  - Paths, collections
- REST is descriptive, not prescriptive!
  - 20 years old (Fielding 2000: Representational State Transfer)
  - _Resources_ (nouns)
  - _Identifiers_ (URI) for resources
  - _Representations_ (JSON) of resources (media types); the Accept header (<- use yaml!)
  - Stateless
  - Hypermedia
  - HATEOAS
    - [Link header](https://www.w3.org/wiki/LinkHeader)
  - [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html)
  - Operations
    - POST, PUT, PATCH

- Status Codes
  - Client side (4xx) vs server side (5xx)
- Filtering, sorting, pagination (<- stateless by using ordered set in Redis)
- Versioning
  - Explicit vs implicit: 
    - Similar to static vs dynamic typing. Also relate to schema vs HATEOAS.
    - Adding fields to an existing API is quite different from designing a totally different one
    - Explicit versions are very expensive
    - Also depends on your goals: A public API (e.g. GitHub) has much different considerations from a private one used inside a company.
    - Contract tests are important here!
  - Options:
    - No versioning
    - URI versioning (/v2)
    - Query string (?version=2)
    - Header (Version: 2)
    - Media type (Accept: application/vnd.github.v3+json)

Testing!
  - Unit
  - Component
  - Contract

Important subjects:


## Sync vs Async APIs - how to build good ones

- [Cancel tokens](https://vorpus.org/blog/timeouts-and-cancellation-for-humans/)
- Exercise: Build an API that can receive a request, report on its status and cancel it.

## Concurrent operations

- *Concurrency*: How do we test it? By serializing the execution of the flow.
  - Example: Read/modify/write: Create a BDB, modify it and write it back. In the meantime, modify it out of context (via a test-specific API?) and ensure the test fails to update it by using a generation or a hash.
  - Similar to the `cluster_state_id` approach in the cnm code, but this is per object.