import time

import requests
from requests.exceptions import HTTPError
from loguru import logger
from exceptions import EmptyPageException


def save_html(content):
    with open('test.html', 'w', encoding='utf') as f:
        f.write(content)


class Requester:
    def __init__(self, ua):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': ua,
                                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                                # 'cookies': cookie
                                }

    def get(self, url):
        for i in range(2):
            resp = self.session.get(url, timeout=5, allow_redirects=False)

            if resp.status_code == 502:
                raise EmptyPageException

            try:
                resp.raise_for_status()

            except HTTPError:
                logger.error(f'[{resp.status_code}] {url} - invalid server response')
                time.sleep(300)
            else:
                logger.debug(f'{url} - html received, status code: {resp.status_code}')
                break

            save_html(resp.text)

        return resp.text


def main():
    url = 'https://www.olx.kz/d/moda-i-stil/naruchnye-chasy/alma-ata/?search%5Bdistrict_id%5D=5&search%5Bprivate_business%5D=private&page=1'

    req = Requester('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36')

    resp = req.get(url)

    with open('test.html', 'w', encoding='utf-8') as f:
        f.write(resp)

    print(resp)

if __name__ == '__main__':
    main()