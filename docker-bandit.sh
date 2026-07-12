#!/bin/bash
set -xe

SRC=${1:-src}

docker run --rm -v $(pwd):/src -w /src python:3.7-slim \
  bash -c "pip install -q bandit && bandit -r ${SRC} -ll"
