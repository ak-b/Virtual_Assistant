#!/bin/sh

set -x
image=registry-qa.webex.com/marvin:test7
docker build -t $image .
docker push $image