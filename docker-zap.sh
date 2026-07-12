#!/bin/bash
set -xe

IMAGE_NAME=$1
TARGET_URL=${2:-http://host.docker.internal:8081}

docker rm -f pycalc-dast || true
docker run -d --rm --name pycalc-dast -p 8081:8081 ${IMAGE_NAME}

sleep 5

mkdir -p zap-reports
chmod 777 zap-reports

docker run --rm \
  -v $(pwd)/zap-reports:/zap/wrk/:rw \
  --add-host=host.docker.internal:host-gateway \
  zaproxy/zap-stable zap-baseline.py \
  -t ${TARGET_URL} \
  -r dast-report.html \
  -I

docker rm -f pycalc-dast
