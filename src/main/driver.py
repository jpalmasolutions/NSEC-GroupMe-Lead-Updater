import json
import os
from src.main.utils.aws import get_user_query
from src.main.utils.logs import logger
from src.main.utils.groupme import update_chat
from src.main.utils.twilio import send_message
from src.main.message.message_obj import Message
import traceback

def lambda_handler(event,context):
    logger.info(json.dumps(event))
    if event:
        try:
            raw_message = event['Records'][0]['Sns']['Message']
            event_msg = json.loads(raw_message)
            
            message = Message(event_msg.get('ID'))
            if message.id:
                message.populate_message()
                sales_rep = message.data.get('SalesRep').split(' ')
                canvasser = message.data.get('Canvasser').split(' ')
                sales_rep_info = get_user_query(sales_rep[0],sales_rep[1])
                canvasser_info = get_user_query(canvasser[0],canvasser[1])

                if message.data.get('Status').strip().upper() == 'LEAD':
                    message.generate_attachments_dropbox()
                    message.generate_text()
                    message.format_text()

                    try:                
                        logger.info(sales_rep_info)
                        logger.info(canvasser_info)
                        to = sales_rep_info.get('Number')
                        origin = os.environ.get('TWILIO_FROM')
                        send_message(message,to,origin)
                    except Exception as te:
                        traceback.print_exc()
                        logger.info(te)

                    try:
                        update_chat(message)
                    except Exception as ge:
                        traceback.print_exc()
                        logger.info(ge)
                else:
                    logger.info('Not a lead, but a %s' % message.get('Data').get('Status').strip().upper())
            else:
                logger.info('Nothing to do, no ID in sns message.')

        except Exception as e:
            traceback.print_exc()
            logger.error(str(e))