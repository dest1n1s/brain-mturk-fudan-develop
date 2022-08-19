"""Module sets qualifications from results csv files"""
import argparse
from client import get_client, get_balance
from pprint import pprint
from process_answer import get_answer
import pandas as pd
import csv, sys
import json
import botocore.exceptions

def set_qualifications(csv_files=[], excel_files=[], qual_id=None, sandbox=False, value=1):
    client = get_client(sandbox=sandbox)

    for file in excel_files or []:
        df = pd.read_excel(file, sheet_name='Sheet1')

        for worker_id in df['WorkerId']:
            try:
                client.associate_qualification_with_worker(QualificationTypeId=qual_id,
                                                           WorkerId=worker_id,
                                                           IntegerValue=value,
                                                           SendNotification=False)
            except botocore.exceptions.ParamValidationError:
                print(f"Parameter validation error updating qualification id {qual_id} for worker id {worker_id}")
                continue
            except botocore.exceptions.ClientError:
                print(f"ClientError error updating qualification id {qual_id} for worker id {worker_id}")
                continue

    for file in csv_files or []:
        df = pd.read_csv(file)

        for worker_id in df['WorkerId']:
            try:
                client.associate_qualification_with_worker(QualificationTypeId=qual_id,
                                                           WorkerId=worker_id,
                                                           IntegerValue=1,
                                                           SendNotification=False)
            except botocore.exceptions.ParamValidationError:
                print(f"Parameter validation error updating qualification id {qual_id} for worker id {worker_id}")
                continue
            except botocore.exceptions.ClientError:
                print(f"ClientError error updating qualification id {qual_id} for worker id {worker_id}")
                continue

            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the results from a HIT.')

    parser.add_argument('--csv', dest='csv', action='append', help='input csv file (can be multiple)')
    parser.add_argument('--excel', dest='excel', action='append', help='input Excel file (can be multiple)')
    parser.add_argument('--qual_id', dest='qual_id', help='Qualification ID', required=True)
    parser.add_argument('--sandbox', dest='sandbox', action='store_true', help='Whether to use the sandbox')

    args = parser.parse_args()
    
    set_qualifications(csv_files=args.csv, excel_files=args.excel, qual_id=args.qual_id, sandbox=args.sandbox)
