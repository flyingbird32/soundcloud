import requests
import json
from utils.logger import log
from utils.tools import obfuscate_auth

class WebhookService:
    def __init__(self, config):
        self.webhook_url = config.get("webhook_url")
        self.should_use_webhook = config.get("use_webhook")

    def send_webhook(self, username, auth, ms):
        if not self.should_use_webhook:
            return

        embed = {
            "title": f"🌥️ claimed `/{username}` in **{ms}ms**",
            "description": f"**token:** {obfuscate_auth(auth).replace("*", "#")}\n**url:** https://soundcloud.com/{username}",
            "color": 16763904
        }

        payload = {
            "embeds": [embed]
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(self.webhook_url, data=json.dumps(payload), headers=headers)
        if response.status_code != 204:
            log("something went wrong when sending webhook", "error")