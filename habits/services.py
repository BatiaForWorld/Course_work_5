import requests
from django.conf import settings


def _telegram_request(method, payload=None):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return None

    url = f'https://api.telegram.org/bot{bot_token}/{method}'
    try:
        response = requests.post(url, json=payload or {}, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None


def send_telegram_message(chat_id, text):
    if not settings.TELEGRAM_BOT_TOKEN or not chat_id:
        return False

    data = _telegram_request('sendMessage', {'chat_id': chat_id, 'text': text})
    return bool(data and data.get('ok'))


def get_bot_info():
    return _telegram_request('getMe')
