#!/bin/bash

if [ "$1" = "snapshot" ]
then
echo 'snapshot tag and push'
docker tag kongrego kongrego:latest
docker push kongrego:latest
fi

if [ "$1" = "release" ]
then
echo 'release tag and push ...'
docker tag kongrego kongrego:stable
docker push kongrego:stable
fi
