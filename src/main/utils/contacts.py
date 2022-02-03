from google.oauth2 import service_account
from googleapiclient.discovery import build
from src.main.utils.logs import logger

def test():
    SCOPES = ['https://www.googleapis.com/auth/directory.readonly','https://www.googleapis.com/auth/contacts']
    SERVICE_ACCOUNT_FILE = 'service_account.json'
    DELEGATE = 'admin@nationalsolarenergycampaign.com'

    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    credentials_delegated = credentials.with_subject(DELEGATE)

    service = build('people', 'v1', credentials=credentials_delegated)

    response = service.people().listDirectoryPeople(readMask='names,emailAddresses',sources='DIRECTORY_SOURCE_TYPE_DOMAIN_CONTACT').execute()

    logger.info(response)