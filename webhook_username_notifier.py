
import requests
import time
from datetime import datetime
import os

# Load webhook URL from environment variable
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Keep track of usernames already notified
already_sent = set()

# Check if Roblox username is available
def is_username_available(username):
    url = f"https://api.roblox.com/users/get-by-username?username={username}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return 'Id' not in data
    return False

# Send styled Discord embed via webhook
def send_webhook_notification(username):
    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    data = {
        "embeds": [
            {
                "title": "🟩 Roblox Username Available",
                "description": f"**Username:** `{username}`\n✅ **Status:** Available",
                "color": 5763719,  # Green color
                "footer": {"text": f"Checked at {now}"}
            }
        ]
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"Failed to send webhook: {response.status_code} - {response.text}")

# Main loop to continuously check usernames
def main():
    while True:
        try:
            with open("usernames.txt", "r") as file:
                usernames = [line.strip() for line in file if line.strip()]
        except Exception as e:
            print(f"Error reading usernames.txt: {e}")
            return

        for username in usernames:
            if username not in already_sent and is_username_available(username):
                send_webhook_notification(username)
                already_sent.add(username)
            time.sleep(1)  # Avoid rate limiting

        time.sleep(300)  # Wait 5 minutes before next round

if __name__ == "__main__":
    main()
