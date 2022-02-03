from datetime import datetime
from src.main.utils.aws import get_lead_item,get_secret
from src.main.utils.logs import logger
class Message():

    groupme_secrets = get_secret('groupme')
    twilio_secrets = get_secret('twilio')

    def __init__(self,id):
        self.id = id

    def populate_message(self):
        item = get_lead_item(self.id)
        # logger.info(item)
        self.data = item.get('Data')
        self.attachments = []
        self.text_format = {}
        self.texts = []

    def generate_attachments_dropbox(self):
        lead = self.data
        file_map = lead.get('Files')

        for k in file_map.keys():
            self.attachments.append(file_map.get(k).get('dbx'))

    def generate_text(self):
        lead = self.data
        appointment = lead.get('Appointment')

        appt_time = datetime.strptime(appointment,'%Y-%m-%dT%H:%M:%S-05:00').strftime('%a %m/%d %I:%M %p')

        appointment_text = 'Appointment Info:\nCanvasser - {canvasser}\nSales Rep - {sales_rep}\nType of Lead - {tol}\nAppointment Time - {appt_time}'.format(
            canvasser=lead.get('Canvasser',''),
            sales_rep=lead.get('SalesRep',''),
            tol=lead.get('LeadType',''),
            appt_time=appt_time
        )

        lead_text = 'Lead Info:\nName - {fname} {lname}\nPhone - {phone}\nEmail - {email}\nAddress - \n{street}\n{city},{state} {zip}'.format(
            fname=lead.get('FirstName',''),
            lname=lead.get('LastName',''),
            phone=lead.get('PhoneNumber','None'),
            email=lead.get('EmailAddress','None'),
            street=lead.get('Street',''),
            city=lead.get('City',''),
            state=lead.get('State',''),
            zip=lead.get('PostalCode','')
        )

        notes_text = 'Notes:\n{notes}'.format(notes=lead.get('Notes','None'))

        images_text = ''
        for attachment in self.attachments:
            if images_text:
                images_text = '{curr}\n\n{link}'.format(curr=images_text,link=attachment)
            else:
                images_text = attachment

        if images_text:
            images_text = 'Images:\n{images}'.format(images=images_text)

        self.text_format['Appointment'] = (appointment_text,len(appointment_text))
        self.text_format['Lead'] = (lead_text,len(lead_text))
        self.text_format['Notes'] = (notes_text,len(notes_text))
        self.text_format['Images'] = (images_text,len(images_text))

    def format_text(self):
        
        texts = []

        # logger.info(self.text_format)

        if self.text_format.get('Notes')[1] < 600:
            if self.text_format.get('Images')[1] > 0:
                text = '{a}\n\n{b}\n\n{c}\n\n{d}'.format(
                    a=self.text_format.get('Appointment')[0],
                    b=self.text_format.get('Lead')[0],
                    c=self.text_format.get('Images')[0],
                    d=self.text_format.get('Notes')[0]
                    )
            else:
                text = '{a}\n\n{b}\n\n{c}'.format(
                    a=self.text_format.get('Appointment')[0],
                    b=self.text_format.get('Lead')[0],
                    c=self.text_format.get('Notes')[0]
                    )
            texts.append(text)
        else:
            text_a = '(1/2)\n{a}\n\n{b}\n\n{c}'.format(
                a=self.text_format.get('Appointment')[0],
                b=self.text_format.get('Lead')[0],
                c=self.text_format.get('Images')[0]
            )

            text_b = '(2/2)\n{d}'.format(
                d=self.text_format.get('Notes')[0]
            )

            texts.append(text_a)
            texts.append(text_b)

        self.texts = texts