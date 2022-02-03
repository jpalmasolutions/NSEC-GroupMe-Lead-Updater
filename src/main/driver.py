import json
import os
from src.main.utils.aws import get_user_item,get_user_query
from src.main.utils.logs import logger
from src.main.utils.groupme import update_chat
from src.main.utils.twilio import send_message
from src.main.utils.user import USER_MAP
from src.main.message.message_obj import Message
# from src.main.utils.sendgrid import send_test
# from src.main.utils.contacts import test
import traceback

def lambda_handler(event,context):

    # logger.info(json.dumps(event))
    if event:
        try:
            raw_message = event['Records'][0]['Sns']['Message']
            event_msg = json.loads(raw_message)
            
            message = Message(event_msg.get('ID'))
            if message.id:
                message.populate_message()
                if message.data.get('Status').strip().upper() == 'LEAD':
                    # attachments = generate_attachments_groupme(lead,groupme_secrets.get('API_KEY'))
                    message.generate_attachments_dropbox()
                    message.generate_text()
                    message.format_text()

                    try:
                        sales_rep = message.data.get('SalesRep').split(' ')
                        user = get_user_query(sales_rep[0],sales_rep[1]).pop()
                        logger.info(user)
                        # to = user.get('Number')
                        # origin = os.environ.get('TWILIO_FROM')
                        # send_message(message,to,origin)
                    except Exception as te:
                        traceback.print_exc()
                        logger.info(te)

                    # try:
                    #     update_chat(message)
                    # except Exception as ge:
                    #     traceback.print_exc()
                    #     logger.info(ge)
                else:
                    logger.info('Not a lead, but a %s' % message.get('Data').get('Status').strip().upper())
            else:
                logger.info('Nothing to do, no ID in sns message.')

        except Exception as e:
            traceback.print_exc()
            logger.error(str(e))