#!/bin/bash

# Image Name
IMAGE_NAME="volatibot:latest"

echo "Building docker image"
docker build -t $IMAGE_NAME .