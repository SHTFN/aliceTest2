from flask import Flask, request, jsonify
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

sessionStorage = {}

creatures = ['слон', 'кролик']


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return jsonify(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Не хочу.",
                "Не буду.",
                "Отстань!",
            ]
        }
        res['response']['text'] = f'Привет! Купи {creatures[0]}а!'
        res['response']['buttons'] = get_suggests(user_id)
        return

    if (('ладно' in req['request']['original_utterance'].lower()
         or 'куплю' in req['request']['original_utterance'].lower()
         or 'покупаю' in req['request']['original_utterance'].lower()
         or 'хорошо' in req['request']['original_utterance'].lower())
            and 'нет' not in req['request']['original_utterance'].lower()
            and 'не' not in req['request']['original_utterance'].lower()):
        res['response']['text'] = f'{creatures[0]}а можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return

    res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи {creatures[0]}а!"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    global creatures
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]

    session['suggests'] = session['suggests'][1:]
    sessionStorage[user_id] = session

    if len(suggests) < 2:
        suggests.append({
            "title": "Ладно",
            "url": f"https://market.yandex.ru/search?text={creatures[0]}",
            "hide": True
        })
        creatures = creatures[1:]

    return suggests


if __name__ == '__main__':
    app.run()
