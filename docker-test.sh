#!/bin/bash
set +e

docker rm -f pycalc-demo
docker run -d --rm --name pycalc-demo -p 8081:8081 mario21ic/pycalc:v1.0

sleep 5

curl localhost:8081

docker rm -f pycalc-demo

