# About

This is a just a simple implementation of a VERY SIMPLISTIC in-memory url-shortener.
It was done as a practice of python syntax, FastAPI and unit testing

## How to run

This project uses [uv](https://github.com/astral-sh/uv) to manage it's packages:

```
# to download dependencies
uv sync
```

```
# to start venv
source .venv/bin/activate
```

```
# to start FastAPI server (defaults to port 8000)
fastapi dev src/main.py
```

check http://127.0.0.1:8000/docs for docs

```
# to run tests
./test.sh
```
