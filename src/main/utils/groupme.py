import os
import requests
from src.main.utils.logs import logger
from src.main.message.message_obj import Message

def update_chat(message:Message):
    bot_id = message.groupme_secrets.get('BOT_ID')

    api = "%s/bots/post" % (os.environ.get('GROUPME_API'))
    headers = {}
    headers['Content-Type'] = 'application/json'

    for text in message.texts:
        if text:
            payload = {}
            payload['bot_id'] = bot_id
            payload['text'] = text
            resp = requests.post(api,headers=headers,json=payload)
            logger.info(resp.text)

