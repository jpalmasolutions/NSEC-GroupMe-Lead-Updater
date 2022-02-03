from src.main.utils.aws import get_secret
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_test():
    sendgrid = get_secret('sendgrid')
    api_key = sendgrid.get('API_KEY')

    message = Mail(
        from_email='admin@nationalsolarenergycampaign.com',
        to_emails='jefrypalmamartinez@gmail.com',
        subject='Solar Links Below')
    message.template_id = 'd-4b28cec7e3fe445c9ca0c48d99ea7378'
    try:
        sg = SendGridAPIClient(api_key)
        sg.send(message)
    except Exception as e:
        print(e)