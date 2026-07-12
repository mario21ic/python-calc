#!/bin/bash
set -xe

IMAGE_NAME=$1

docker rm -f pycalc-integration || true
docker run -d --rm --name pycalc-integration -p 8081:8081 ${IMAGE_NAME}

sleep 5

docker run --rm \
  -v $(pwd):/src -w /src \
  --add-host=host.docker.internal:host-gateway \
  -e API_URL=http://host.docker.internal:8081 \
  python:3.7-slim \
  bash -c "pip install -q requests && python -m unittest discover -v -s test/integration"

docker rm -f pycalc-integration
