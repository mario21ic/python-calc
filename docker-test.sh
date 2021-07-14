#!/bin/bash
set -e

docker run -d --rm --name pycalc-demo -p 8081:8081 mario21ic/pycalc:v1.0

curl localhost:8081

docker rm pycalc-demo

