#!/bin/bash

# Image Name
IMAGE_NAME="stock-alert-bot:latest"

echo "Building docker image"
docker build -t $IMAGE_NAME .