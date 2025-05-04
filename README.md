# VolatiBot

Receive real-time Discord notifications (messages are in French by default — customizable in `variation_checker.py`) when your selected stocks vary by a specified percentage since the last market close.



## Build the Docker image

In the root folder, run:

```bash
./build-image.sh
```


## Run the Docker container

### Option 1: Using the provided script

Set your environment variables (`TICKERS`, `ALERT_LEVELS`, `DISCORD_WEBHOOK_URL`) inside `run-containerized-app.sh`, then launch the script:

```bash
./run-containerized-app.sh
```

---

### Option 2: Using `docker run`

```bash
docker run -d \
  -e TICKERS="AAPL,MSFT,AMZN,GOOG,META" \
  -e ALERT_LEVELS="5,10,15" \
  -e DISCORD_WEBHOOK_URL="https://your-webhook-url" \
  --name stock-variation-alert-app \
  $IMAGE_NAME
```

---

### Option 3: Using Docker Compose

```yaml
services:
  stock-variation-alert-app:
    image: $IMAGE_NAME
    container_name: stock-variation-alert-app
    environment:
      - TICKERS=AAPL,MSFT,AMZN,GOOG,META  # Format: uppercase symbols separated by commas
      - ALERT_LEVELS=5,10,15              # Format: percentage thresholds separated by commas
      - DISCORD_WEBHOOK_URL=https://your-webhook-url
      - CHECK_INTERVAL=600               # Run checks every 600 seconds (10 minutes)
    restart: unless-stopped
```
