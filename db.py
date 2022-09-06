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

        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS stop_words (
        word	TEXT NOT NULL UNIQUE)""")

        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS black_list (
        id	TEXT NOT NULL UNIQUE)""")

        self.connection.execute("""
        CREATE TABLE IF NOT EXISTS categories (
        url	TEXT NOT NULL UNIQUE)""")

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

    def add_stopword(self, word: str):
        logger.debug('Adding stopword in db..')
        try:
            self.cursor.execute("INSERT INTO stop_words VALUES(?)", (word,))
        except IntegrityError:
            logger.error('Failed to add a stopword in db')

        else:
            logger.debug('Stopword has been added')
            self.connection.commit()

    def remove_stopword(self, word: str):
        logger.debug('Removing a stopword from db..')
        self.cursor.execute("DELETE FROM stop_words WHERE word == ?", (word,))
        self.connection.commit()
        logger.debug('Category has been removed')

    def get_stopwords(self) -> List:
        logger.debug('Getting stopwords from db')
        resp = self.cursor.execute("SELECT id FROM stop_words").fetchall()
        return [d[0] for d in resp]

#======================

    def add_to_blacklist(self, user_id: str):
        logger.debug('Adding id in blacklist..')
        try:
            self.cursor.execute("INSERT INTO stop_words VALUES(?)", (user_id,))
        except IntegrityError:
            logger.error('Failed to add id in blacklist')

        else:
            logger.debug('Id has been added in blacklist')
            self.connection.commit()

    def remove_from_blacklist(self, user_id: str):
        logger.debug('Removing id from blacklist..')
        self.cursor.execute("DELETE FROM black_list WHERE id == ?", (user_id,))
        self.connection.commit()
        logger.debug('Id has been removed from blacklist')

    def get_blacklist(self) -> List:
        logger.debug('Getting ids from black_list')
        resp = self.cursor.execute("SELECT id FROM black_list").fetchall()
        return [d[0] for d in resp]