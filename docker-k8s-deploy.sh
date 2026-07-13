#!/bin/bash
set -xe

IMAGE_NAME=$1
NAMESPACE=${2:-default}
KUBECONFIG_PATH=$3

RENDERED=k8s/deployment.rendered.yaml
sed "s|__IMAGE__|${IMAGE_NAME}|g" k8s/deployment.yaml > ${RENDERED}
trap 'rm -f ${RENDERED}' EXIT

docker run --rm \
  -v $(pwd)/k8s:/manifests:ro \
  -v ${KUBECONFIG_PATH}:/.kube/config:ro \
  -e KUBECONFIG=/.kube/config \
  bitnami/kubectl:latest \
  apply -n ${NAMESPACE} -f /manifests/deployment.rendered.yaml -f /manifests/service.yaml

docker run --rm \
  -v ${KUBECONFIG_PATH}:/.kube/config:ro \
  -e KUBECONFIG=/.kube/config \
  bitnami/kubectl:latest \
  rollout status -n ${NAMESPACE} deployment/python-calc --timeout=120s
