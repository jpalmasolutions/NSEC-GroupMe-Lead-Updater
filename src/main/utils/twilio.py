from src.main.message.message_obj import Message
from src.main.utils.logs import logger
from twilio.rest import Client

def send_message(message:Message,to,origin):
    twilio_secrets = message.twilio_secrets
    client = Client(twilio_secrets['Twilio_SID'], twilio_secrets['Twilio_AUTH'])

    for text in message.texts:
        if text:
            response = client.messages.create(
                to=to,
                from_=origin,
                body=text)

            logger.info(response.sid)