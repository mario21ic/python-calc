#!/bin/bash
set -x
IMAGE_NAME=$1

docker run --rm \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v $HOME/.cache:/root/.cache \
    aquasec/trivy:latest image --severity HIGH,CRITICAL ${IMAGE_NAME}
    # aquasec/trivy:latest image --exit-code 1 --severity HIGH,CRITICAL ${IMAGE_NAME}
