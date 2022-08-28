# from configparser import ConfigParser
import os

# config = ConfigParser()
# config.read('settings.ini')


# user_agent = config['App']['user_agent']
# api_parser_token = config['App']['api_parser_token']
# bot_api_token = config['Telegram']['bot_api_token']
# telegram_api_address = config['Telegram']['telegram_api_address']
# interaval = config['App']['interval']

user_agent = os.getenv('user_agent')
api_parser_token = os.getenv('api_parser_token')
bot_api_token = os.getenv('bot_api_token')
telegram_api_address = os.getenv('telegram_api_address')
interaval = os.getenv('interval')