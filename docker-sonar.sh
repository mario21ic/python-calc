#!/bin/bash
set -euo pipefail

# Si no hay token, no fallamos el pipeline; solo omitimos el scan
if [ -z "${SONAR_TOKEN:-}" ]; then
  echo "SONAR_TOKEN no esta definido. Omitiendo Sonar scan."
  exit 0
fi

SONAR_ORGANIZATION=$1
SONAR_PROJECT_KEY=$2
SONAR_HOST_URL=${3:-https://sonarcloud.io}

docker run --rm \
  -v $(pwd):/usr/src \
  -w /usr/src \
  sonarsource/sonar-scanner-cli:latest \
  -Dsonar.organization=${SONAR_ORGANIZATION} \
  -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
  -Dsonar.host.url=${SONAR_HOST_URL} \
  -Dsonar.token=${SONAR_TOKEN} \
  -Dsonar.sources=src \
  -Dsonar.python.version=3.7
