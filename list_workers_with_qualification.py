import argparse
from client import get_client
from pprint import pprint

import pandas as pd


def list_workers_with_qualification(qualification_id, output, sandbox=False):
    dfs = []
    go = True
    next_token = None
    while go:
        if next_token is not None:
            response = get_client(sandbox=sandbox).list_workers_with_qualification_type(QualificationTypeId=qualification_id,
                                                                                        MaxResults=100,
                                                                                        NextToken=next_token)
        else:
            response = get_client(sandbox=sandbox).list_workers_with_qualification_type(QualificationTypeId=qualification_id,
                                                                                        MaxResults=100)

        workers = response.get('Qualifications',[])
        df = pd.DataFrame(workers)

        df2 = df[['WorkerId']]
        dfs.append(df2)
        if response.get('NumResults',0) == 100:
            next_token = response.get('NextToken', None)
            if next_token is None:
                go = False
        else:
            go = False

    df = pd.concat(dfs)
    df.to_csv(output, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List workers with a qualification.')

    parser.add_argument('--qualification_id', dest='qualification_id', help='Qualification ID', default=None)
    parser.add_argument('--output', dest='output', help='Output csv file', default='workers.csv')
    parser.add_argument('--sandbox', dest='sandbox', action='store_true', help='Whether to use the sandbox')

    args = parser.parse_args()

    list_workers_with_qualification(args.qualification_id, args.output, sandbox=args.sandbox)
