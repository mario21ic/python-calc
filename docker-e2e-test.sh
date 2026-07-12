#!/bin/bash
set -xe

IMAGE_NAME=$1

docker rm -f pycalc-e2e || true
docker run -d --rm --name pycalc-e2e -p 8081:8081 ${IMAGE_NAME}

sleep 5

docker run --rm \
  -v $(pwd):/src -w /src \
  --add-host=host.docker.internal:host-gateway \
  -e API_URL=http://host.docker.internal:8081 \
  python:3.7-slim \
  bash -c "pip install -q requests && python -m unittest discover -v -s test/e2e"

docker rm -f pycalc-e2e
