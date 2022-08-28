from offer import Offer
from settings import telegram_api_address, bot_api_token
from requests.exceptions import HTTPError
import requests

def send_offer(offer: Offer):
    resp = requests.post(f'http://{telegram_api_address}/offer', json={
        'token': bot_api_token,
        'url': offer.url,
        'title': offer.title,
        'id': offer.id,
        'description': offer.description,
        'price': offer.price,
        'img_url': offer.img_url
    }, timeout=1)

    if resp.status_code != 200:
        raise HTTPError(f'Неверный ответ сервера, статус код: {resp.status_code}')


