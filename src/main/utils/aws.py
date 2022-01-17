import boto3
import base64
from botocore.exceptions import ClientError
import json
import os
from src.main.utils.logs import logger

def get_secret(secret_name):
    region_name = os.environ['REGION']

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            decoded_binary_secret = base64.b64decode(
                get_secret_value_response['SecretBinary'])
            return decoded_binary_secret


def _get_table(table_name):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
    table = dynamodb.Table(table_name)
    return table

def get_lead_item(lead_id):
    table = _get_table(os.environ.get('NSEC_LEADS_TABLE'))
    item = table.get_item(
        Key={
            'ID': lead_id
        }
    )

    if 'Item' in item:
        return item['Item']
    else:
        raise Exception('Item not found for execution id: %s' % lead_id)

def get_user_item(email):
    table = _get_table(os.environ.get('NSEC_USER_TABLE'))
    item = table.get_item(
        Key={
            'Email': email
        }
    )

    if 'Item' in item:
        return item['Item']
    else:
        raise Exception('Item not found for execution id: %s' % email)

def get_object(s3_uri):
    s3_client = boto3.client('s3')
    
    temp = str(s3_uri).removeprefix('s3://')
    s3_split = temp.split('/',1)
    bucket = s3_split[0]
    key = s3_split[1]

    response = s3_client.get_object(
        Bucket = bucket,
        Key = key
    )

    logger.info(response)

    return response.get('Body')
        