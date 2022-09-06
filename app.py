import time
from waitress import serve
from flask import Flask, jsonify, request
from loader import db
from loguru import logger
from settings import api_parser_token, interaval
from olx import OlxParser
from requester import Requester
import threading

app = Flask(__name__)

client = app.test_client()


# @app.route('/categories', methods=['GET'])
# def get_list():
#     return jsonify(test_data)

@app.route('/categories', methods=['POST'])
def add_category():
    logger.debug('[POST] Request to adding/removing category')

    request_json = request.get_json()
    requests_token = request_json.get('token', '')
    if requests_token == api_parser_token:
        try:
            cmd = request_json['cmd']
            url = request_json['url'].replace('m.', '')
        except KeyError:
            logger.warning('[POST] Bad request, url or cmd is empty')
            return jsonify({'status': 'ERROR'}), 400
        else:

            if cmd.lower() == 'add':
                db.add_category(url)
                return jsonify({'status': 'OK', 'cmd': cmd.lower()}), 200

            elif cmd.lower() == 'remove':
                db.remove_category(url)
                return jsonify({'status': 'OK', 'cmd': cmd.lower()}), 200
            else:
                logger.warning('[POST] Bad request, unknown cmd')
                return jsonify({'status': 'ERROR', 'cmd': cmd.lower()}), 400

    else:
        return jsonify({'status': 'access denied'}), 401


@app.route('/categories', methods=['GET'])
def get_categories():
    logger.debug('[GET] Request to get categories')
    request_json = request.get_json()
    requests_token = request_json.get('token', '')

    if requests_token == api_parser_token:
        return jsonify({'categories': db.get_categories()}), 200
    else:
        return jsonify({'status': 'access denied'}), 401


@app.route('/stopwords', methods=['POST'])
def stopword_post():
    logger.debug('[POST] Request to adding/removing stopword')

    request_json = request.get_json()
    requests_token = request_json.get('token', '')
    if requests_token == api_parser_token:
        try:
            cmd = request_json['cmd']
            word = request_json['word']
        except KeyError:
            logger.warning('[POST] Bad request, word or cmd is empty')
            return jsonify({'status': 'ERROR'}), 400
        else:

            if cmd.lower() == 'add':
                db.add_stopword(word)
                return jsonify({'status': 'OK', 'cmd': cmd.lower()}), 200

            elif cmd.lower() == 'remove':
                db.remove_stopword(word)
                return jsonify({'status': 'OK', 'cmd': cmd.lower()}), 200
            else:
                logger.warning('[POST] Bad request, unknown cmd')
                return jsonify({'status': 'ERROR', 'cmd': cmd.lower()}), 400

    else:
        return jsonify({'status': 'access denied'}), 401


@app.route('/stopwords', methods=['GET'])
def get_stopwords():
    logger.debug('[GET] Request to get stopwords')
    request_json = request.get_json()
    requests_token = request_json.get('token', '')

    if requests_token == api_parser_token:
        return jsonify({'categories': db.get_stopwords()}), 200
    else:
        return jsonify({'status': 'access denied'}), 401


@app.route('/blacklist', methods=['POST'])
def blacklist_post():
    logger.debug('[POST] Request to adding/removing from blacklist')

    request_json = request.get_json()
    requests_token = request_json.get('token', '')
    if requests_token == api_parser_token:
        try:
            cmd = request_json['cmd']
            user_id = request_json['user_id']
        except KeyError:
            logger.warning('[POST] Bad request, user_id or cmd is empty')
            return jsonify({'status': 'ERROR'}), 400
        else:

            if cmd.lower() == 'add':
                db.add_to_blacklist(user_id)
                return jsonify({'status': 'OK', 'cmd': cmd.lower()}), 200

            elif cmd.lower() == 'remove':
                db.remove_from_blacklist(user_id)
                return jsonify({'status': 'OK', 'cmd': cmd.lower()}), 200
            else:
                logger.warning('[POST] Bad request, unknown cmd')
                return jsonify({'status': 'ERROR', 'cmd': cmd.lower()}), 400

    else:
        return jsonify({'status': 'access denied'}), 401


@app.route('/blacklist', methods=['GET'])
def get_blacklist():
    logger.debug('[GET] Request to get blacklist')
    request_json = request.get_json()
    requests_token = request_json.get('token', '')

    if requests_token == api_parser_token:
        return jsonify({'categories': db.get_blacklist()}), 200
    else:
        return jsonify({'status': 'access denied'}), 401


def target():
    logger.info('Server has been started..')
    return serve(app, host="0.0.0.0", port=8080)


@logger.catch
def main():
    t = threading.Thread(target=target, daemon=True)
    t.start()

    olx = OlxParser()

    while True:
        for url in db.get_categories():
            olx.check_category(url)
        time.sleep(int(interaval))

    t.join()


if __name__ == '__main__':
    main()
