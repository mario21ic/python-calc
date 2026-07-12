#!/bin/bash
set -xe

REQUIREMENTS=${1:-requirements.txt}

docker run --rm -v $(pwd):/src -w /src python:3.7-slim \
  bash -c "pip install -q pip-audit && pip-audit -r ${REQUIREMENTS}"
