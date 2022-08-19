"""
Getting mturk client
"""
import argparse
import boto3
from dotenv import load_dotenv

load_dotenv(override=True)  # take environment variables from .env.

from pprint import pprint
import os
import pandas as pd


def get_balance(client):
    pprint(client.get_account_balance())
    return client.get_account_balance().get('AvailableBalance')


def get_mturk_client(aws_access_key_id, aws_secret_access_key, sandbox=False):
    if sandbox:
        endpoint_url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'
    else:
        endpoint_url = 'https://mturk-requester.us-east-1.amazonaws.com'
    return boto3.client(
        'mturk',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        endpoint_url=endpoint_url,
        region_name='us-east-1',
    )


aws_key = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret = os.environ.get('AWS_SECRET_ACCESS_KEY')


def get_client(sandbox=False):
    return get_mturk_client(aws_access_key_id=aws_key, aws_secret_access_key=aws_secret, sandbox=sandbox)

def list_hits(client, file):
    response = client.list_hits()

    hits = response.get('HITs', [])
    df = pd.DataFrame(hits)

    # ['HITId', 'HITTypeId', 'HITGroupId', 'CreationTime', 'Title',
    #   'Description', 'Question', 'Keywords', 'HITStatus', 'MaxAssignments',
    #   'Reward', 'AutoApprovalDelayInSeconds', 'Expiration',
    #   'AssignmentDurationInSeconds', 'QualificationRequirements',
    #   'HITReviewStatus', 'NumberOfAssignmentsPending',
    #   'NumberOfAssignmentsAvailable', 'NumberOfAssignmentsCompleted']
       
    df2 = df[['HITId', 'Title', 'CreationTime', 'Expiration',
              'Description', 'HITStatus', 'Reward', 'NumberOfAssignmentsAvailable',
              'NumberOfAssignmentsPending',
              'NumberOfAssignmentsCompleted',
              'MaxAssignments']]
    
    df2.to_csv(file, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a new HIT.')

    parser.add_argument('--sandbox', dest='sandbox', action='store_true', help='Whether to use the sandbox')
    parser.add_argument('--output', dest='output', help='Output csv file', required=True)

    args = parser.parse_args()

    client = get_client(sandbox=args.sandbox)
    list_hits(client, args.output)
