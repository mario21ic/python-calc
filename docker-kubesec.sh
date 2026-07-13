#!/bin/bash
set -uo pipefail

MANIFEST=${1:-k8s/deployment.yaml}
MIN_SCORE=${2:-0}

# kubesec's own exit code isn't a reliable pass/fail signal, so it's ignored
# here and the score from its JSON output is checked explicitly below.
RESULT=$(docker run --rm -i --platform linux/amd64 kubesec/kubesec:512c5e0 scan /dev/stdin < "${MANIFEST}") || true
echo "${RESULT}"

SCORE=$(echo "${RESULT}" | docker run --rm -i python:3.7-slim python3 -c "import json,sys; print(json.load(sys.stdin)[0]['score'])")

echo "Kubesec score: ${SCORE} (minimo requerido: ${MIN_SCORE})"

if [ "${SCORE}" -lt "${MIN_SCORE}" ]; then
  echo "El score de kubesec esta por debajo del minimo requerido. Fallando el build."
  exit 1
fi
