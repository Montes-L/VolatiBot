import requests
import os

discord_webhook_url=os.getenv("DISCORD_WEBHOOK_URL")

def send_discord_alert(message: str, webhook_url: str=discord_webhook_url):
    """
    Sends an alert to a Discord channel via a webhook if a variation is detected.

    :param webhook_url: The Discord webhook URL
    :param message: The message to send in the discord channel
    """
    message = {
        "content": f"{message}"
    }

    try:
        response = requests.post(webhook_url, json=message)
        response.raise_for_status()
        print("✅ Alert sent to Discord")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error while sending alert to Discord: {e}")