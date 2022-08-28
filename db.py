import sqlite3
from sqlite3 import IntegrityError
from offer import Offer
from typing import List
from loguru import logger


class DataBase:
    def __init__(self):
        self.connection = sqlite3.connect("data/database.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS viewed_links (
        url	TEXT NOT NULL UNIQUE)""")

        # self.connection.execute("""
        # CREATE TABLE IF NOT EXISTS offers (
        # url TEXT NOT NULL,
        # title TEXT,
        # id TEXT,
        # price TEXT,
        # description TEXT,
        # img_url TEXT,
        # PRIMARY KEY("url"))""")

        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS categories (
        url	TEXT NOT NULL UNIQUE)""")

    # def add_offer(self, offer: Offer):
    #     logger.debug('Adding offer in db..')
    #     request = "INSERT INTO offers VALUES(?,)"
    #     # self.cursor.execute(request, (offer.url, offer.title, offer.id, offer.price, offer.description, offer.img_url))
    #     self.cursor.execute(request, (offer.url,))
    #     self.connection.commit()
    #     logger.debug('Offer has been added')

    def add_to_viewed_links(self, url: str):
        logger.debug('Adding viewed url in db..')
        self.cursor.execute("INSERT INTO viewed_links VALUES(?)", (url,))
        logger.debug('Viewed url has been added')
        self.connection.commit()

    def get_urls(self) -> list:
        logger.debug('Getting urls from db')
        resp = self.cursor.execute("SELECT url FROM viewed_links").fetchall()
        return [d[0] for d in resp]

    # def get_data(self) -> list:
    #     logger.debug('Getting offers from db')
    #     return self.cursor.execute("SELECT * FROM offers").fetchall()

    def add_category(self, url: str):
        logger.debug('Adding category in db..')
        try:
            self.cursor.execute("INSERT INTO categories VALUES(?)", (url,))
        except IntegrityError:
            logger.error('Failed to add a category in db')

        else:
            logger.debug('Category has been added')
            self.connection.commit()

    def remove_category(self, url: str):
        logger.debug('Removing a category from db..')
        self.cursor.execute("DELETE FROM categories WHERE url == ?", (url,))
        self.connection.commit()
        logger.debug('Category has been removed')

    def get_categories(self) -> List:
        logger.debug('Getting categories from db')
        resp = self.cursor.execute("SELECT url FROM categories").fetchall()
        return [d[0] for d in resp]

    def close(self):
        logger.debug('Closing connection')
        self.connection.close()
