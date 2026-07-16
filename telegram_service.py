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

def send_message_to_user(chat_id,text):
    url = f"{config.TELEGRAM_URL_BASE}{config.TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)
