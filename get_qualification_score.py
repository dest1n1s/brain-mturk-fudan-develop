import argparse
from client import get_client
from pprint import pprint

import pandas as pd


def get_qualification_score(worker_id, qualification_id, sandbox=False):
    response = get_client(sandbox=sandbox).get_qualification_score(QualificationTypeId=qualification_id,
                                                                   WorkerId=worker_id)
    print(response)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get qualification score for a worker and a qualification ID.')

    parser.add_argument('--qualification_id', dest='qualification_id', help='Qualification ID', required=True)
    parser.add_argument('--worker_id', dest='worker_id', help='Worker ID', required=True)
    parser.add_argument('--sandbox', dest='sandbox', action='store_true', help='Whether to use the sandbox')

    args = parser.parse_args()

    get_qualification_score(args.worker_id, args.qualification_id, sandbox=args.sandbox)
