import argparse
from client import get_client
from pprint import pprint

import pandas as pd


def list_qualifications(file, sandbox=True):
    response = get_client(sandbox=sandbox).list_qualification_types(MustBeRequestable=False, MustBeOwnedByCaller=True)

    qualifications = response.get('QualificationTypes',[])
    df = pd.DataFrame(qualifications)

    df2 = df[['CreationTime', 'Description', 'IsRequestable', 'Name', 'QualificationTypeId', 'QualificationTypeStatus']]

    df2.to_csv(file, index=False)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List qualifications.')

    parser.add_argument('--output', dest='output', help='Output csv file', default='qualifications.csv')    
    parser.add_argument('--sandbox', dest='sandbox', action='store_true', help='Whether to use the sandbox')

    args = parser.parse_args()

    list_qualifications(args.output, sandbox=args.sandbox)
