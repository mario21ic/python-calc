#!/bin/bash
set -xe

DOCKER_IMAGE=$1

docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  anchore/syft:latest ${DOCKER_IMAGE}
