#!/bin/bash
set -xe

SRC=$1

docker run -v $SRC:/src mario21ic/gittyleaks:v1 gittyleaks --search-only-head
