#!/bin/bash
set -xe

IMAGE_NAME=$1

WORKDIR=$(pwd)/clamav-scan
rm -rf "${WORKDIR}"
mkdir -p "${WORKDIR}/fs"
trap 'rm -rf "${WORKDIR}"' EXIT

CONTAINER_ID=$(docker create ${IMAGE_NAME})
docker export ${CONTAINER_ID} -o "${WORKDIR}/image.tar"
docker rm ${CONTAINER_ID}

tar -xf "${WORKDIR}/image.tar" -C "${WORKDIR}/fs"

CLAMSCAN_EXIT=0
docker run --rm \
  --platform linux/amd64 \
  -v "${WORKDIR}/fs":/scan:ro \
  --entrypoint sh \
  clamav/clamav:latest \
  -c "freshclam --quiet || true; clamscan -r --infected /scan" || CLAMSCAN_EXIT=$?

if [ "${CLAMSCAN_EXIT}" -eq 1 ]; then
  echo "ClamAV: se encontraron archivos infectados."
  exit 1
elif [ "${CLAMSCAN_EXIT}" -ge 2 ]; then
  echo "ClamAV: el scan finalizo con advertencias (exit ${CLAMSCAN_EXIT}, ej. symlinks rotos o permisos al exportar el filesystem), no se detecto malware."
fi
