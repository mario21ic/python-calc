#!/bin/bash
set -xe

docker run -v ./:/src mario21ic/gittyleaks:v1 gittyleaks --search-only-head
