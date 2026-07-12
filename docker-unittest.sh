#!/bin/bash
set -xe

docker run --rm -v $(pwd):/src -w /src python:3.7-slim \
  bash -c "pip install -q -r requirements.txt && coverage run -m unittest discover -v -p 'test_calc.py' && coverage report"
