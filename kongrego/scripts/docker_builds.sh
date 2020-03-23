#!/bin/sh
if [ "$1" = "snapshot" ]
then
docker build . -t kongrego:latest
fi

if [ "$1" = "release" ]
then
docker build . -t kongrego:stable
fi
