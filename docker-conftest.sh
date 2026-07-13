#!/bin/bash
set -xe

MANIFEST=${1:-k8s/deployment.yaml}

docker run --rm \
  -v $(pwd)/${MANIFEST}:/project/manifest.yaml:ro \
  -v $(pwd)/policy:/project/policy:ro \
  -w /project \
  openpolicyagent/conftest:latest \
  test manifest.yaml -p policy
