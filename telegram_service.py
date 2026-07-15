import requests
import config
def get_updates(offset=None):
    url = f"{config.TELEGRAM_URL_BASE}{config.TELEGRAM_TOKEN}/getUpdates"
    params = {
        "timeout": 30
    }
    if offset:
        params["offset"] = offset
    response = requests.get(url, params=params)
    return response.json()

def send_message_to_user(text):
    url = f"{config.TELEGRAM_URL_BASE}{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": config.TELEGRAM_CHAT_ID_BOT,
        "text": text
    }
    requests.post(url, json=payload)
