#!/bin/bash

# Image and container name
IMAGE_NAME="volatibot"
CONTAINER_NAME="volatibot"

export TICKERS="AAPL,MSFT,AMZN,GOOG,META"
export ALERT_LEVELS="5,7.5,10,15"
export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/X/X"
export CHECK_INTERVAL="600"

echo "Launching the container"
docker run -d -e TICKERS=$TICKERS -e ALERT_LEVELS=$ALERT_LEVELS -e DISCORD_WEBHOOK_URL=$DISCORD_WEBHOOK_URL -e CHECK_INTERVAL=$CHECK_INTERVAL --name $CONTAINER_NAME $IMAGE_NAME
