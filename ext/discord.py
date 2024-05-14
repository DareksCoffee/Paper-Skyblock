import requests
import json

class DiscordWebhook:
    def __init__(self):
        self.webhook = "https://discord.com/api/webhooks/1234991231734386778/JTo1JkLlVa3v2he2xR33cy6uodKAVyL56CM4jvYMB5ArFOB3uq2UzorRWrtzu_H8jh20"
    
    def send_message(self, message: str):
        payload = {
            "content": message
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(self.webhook, data=json.dumps(payload), headers=headers)