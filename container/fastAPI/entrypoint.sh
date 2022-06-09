#!/bin/bash

if [ -f pyproject.toml ]; then
    # poetryで利用する環境をGlobalで利用する
    poetry config virtualenvs.in-project true
    poetry install
fi

# poetry経由でのuvicorn起動
poetry run uvicorn api.main:app --host 0.0.0.0 --reload

# Then exec the container's main process (what's set as CMD in the Dockerfile).
exec "$@"
