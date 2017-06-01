import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '386195912:AAFy6E1I8gU--G9mTtezl_td646GFRuq-gs'
WEBHOOK_URL = 'https://33e60252.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'hamburger',
        'fries',
        'for_here',
        'to_go'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'hamburger',
            'conditions': 'is_going_to_hamburger'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'fries',
            'conditions': 'is_going_to_fries'
        },
        {
            'trigger': 'advance',
            'source':  [
                'hamburger',
                'fries'
            ],
            'dest': 'for_here',
            'conditions': 'is_going_to_for_here'
        },
        {
            'trigger': 'advance',
            'source':  [
                'hamburger',
                'fries'
            ],
            'dest': 'to_go',
            'conditions': 'is_going_to_to_go'
        },
        {
            'trigger': 'go_back',
            'source': [
                'for_here',
                'to_go'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
