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
