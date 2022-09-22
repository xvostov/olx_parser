import time

from loguru import logger

import api
from offer import Offer
from loader import requester, db
from bs4 import BeautifulSoup
from exceptions import EmptyPageException, MissingPhotoException, UnsuitableProductError

import re



class OlxParser:
    def __init__(self):
        self.requester = requester
        self.html_cleaner = re.compile('<.*?>')

    def get_offer(self, url) -> Offer:

        logger.debug(f'{url} - parsing..')
        content = self.requester.get(url)
        soup = BeautifulSoup(content, 'lxml')

        seller_id = soup.find_all('a', {'href': re.compile('^/d/list/user/')})[0].get('href')
        seller_id = seller_id.replace('/d/list/user/', '').replace('/', '').strip()

        for user_id in db.get_blacklist():
            if user_id == seller_id:
                raise UnsuitableProductError


        offer = Offer()
        offer.url = url

        logger.debug('title - parsing..')
        with open('test.html', 'w', encoding='utf-8') as f:
            f.write(content)
        offer.title = soup.find_all('h1', {'data-cy': 'ad_title'})[0].text
        logger.debug('title - OK')

        logger.debug('id - parsing..')
        offer.id = soup.find_all('div', {'data-cy':'ad-footer-bar-section'})[0].text.replace('ID: ', '')
        logger.debug('id - OK')

        logger.debug('description - parsing..')
        raw_description = soup.find_all('div', {'data-cy': 'ad_description'})[0].text.replace('Описание', '').strip()
        offer.description = re.sub(self.html_cleaner, '', raw_description)
        logger.debug('description - OK')

        for stop_word in db.get_stopwords():
            if stop_word in offer.title or stop_word in offer.description:
                logger.debug(f'stopword: {stop_word} was found')
                raise UnsuitableProductError

        logger.debug('price - parsing..')
        offer.price = soup.find_all('div', {'data-testid': 'ad-price-container'})[0].text
        logger.debug('price - OK')

        logger.debug('img_url - parsing..')
        try:
            offer.img_url = soup.find_all('div', class_='swiper-zoom-container')[0].find('img').get('src')

        except IndexError:
            logger.debug('img_url - missing')
            raise MissingPhotoException

        logger.debug('img_url - OK')

        logger.info(f'{url} - parsing is successful')
        return offer

    def get_urls(self, url):
        urls_list = []

        for page_num in range(1, 9999):

            logger.info(f'Trying to parse page {page_num}')
            page_url = re.sub(r'&page=\d{0,3}', '', url) + f'&page={page_num}'

            try:
                content = self.requester.get(page_url)

            except EmptyPageException:
                logger.info(f'Last page {page_num - 1}')
                break

            soup = BeautifulSoup(content, 'lxml')

            all_cards = soup.find_all('div', {'class': 'l-card'})
            if len(all_cards) == 0:
                break

            logger.debug(f'Cards found on the page: {len(all_cards)}')
            for card in all_cards:
                offer_url = card.find_all('a')[0].get('href').split('.html#')[0] + '.html'
                urls_list.append(offer_url)
            time.sleep(1)

        logger.debug(f'Url found: {len(urls_list)}')
        urls_list = list(set(urls_list))

        for url in db.get_urls():
            if url in urls_list:
                logger.debug(f'{url} - Url was found in the db, will be skipped')
                urls_list.remove(url)

        logger.debug(f'Filtered urls: {len(urls_list)}')
        return urls_list

    def check_category(self, category_url):
        logger.debug(f'Parsing category - {category_url}')
        urls_list = self.get_urls(category_url)

        for url in db.get_urls():
            if url in urls_list:
                urls_list.remove(url)

        for url in urls_list:
            try:
                offer = self.get_offer(url)
            except UnsuitableProductError:
                logger.warning(f'{url} - will be skipped')
            except MissingPhotoException:
                logger.warning(f'{url} - will be skipped')

            else:
                api.send_offer(offer)
                if offer.url not in db.get_urls():
                    db.add_to_viewed_links(offer.url)
            time.sleep(5)