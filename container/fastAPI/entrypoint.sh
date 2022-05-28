#!/bin/bash

if [[ -z ${PIP_CACHE_DIR} ]];then
    # requirements.txt に定義されているパッケージをインストールする
    pip install -r requirements.txt --quiet
fi

# Then exec the container's main process (what's set as CMD in the Dockerfile).
exec "$@"
