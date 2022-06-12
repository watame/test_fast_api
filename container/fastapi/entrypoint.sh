#!/bin/bash

if [ -f pyproject.toml ]; then
    # poetryで利用する環境をGlobalで利用する
    poetry config virtualenvs.in-project true
    poetry install
fi

# Then exec the container's main process (what's set as CMD in the Dockerfile).
exec "$@"
