"""Module retrieves assignment answers and stores them in a csv"""
import argparse
from client import get_client, get_balance
from pprint import pprint
from process_answer import get_answer
import pandas as pd
import csv, sys
import json


# Source: https://www.beresfordresearch.com/age-range-by-generation/
#	Born	Ages
#Gen Z	1997 – 2012	10 – 25
#Millennials	1981 – 1996	26 – 41
#Gen X	1965 – 1980	42 – 57
#Boomers II*	1955 – 1964	58 – 67
#Boomers I*	1946 – 1954	68 – 76
#Post War	1928 – 1945	77 – 94
#WW II	1922 – 1927	95 – 100

def age_to_generation(age_str):
    age = int(age_str)
    if age < 26:
        return '0 Gen Z'
    elif age < 42:
        return '1 Millennials'
    elif age < 58:
        return '2 Gen X'
    elif age < 68:
        return '3 Boomers II'
    elif age < 77:
        return '4 Boomers I'
    elif age < 95:
        return '5 Post War'
    else:
        return '6 WW II'

readable_dict = {}

readable_dict['shopping_device'] = {
    0: 'Mobile phone',
    1: 'Tablet',
    2: 'Laptop',
    3: 'Desktop',
    4: 'Other',
    999: 'Don\'t Know/Prefer not to say'}

readable_dict['date_last_purchase'] = {
    0: 'Today',
    1: 'Yesterday or day before',
    2: '4 to 7 days ago',
    3: '1 to 3  weeks  ago',
    4: 'About a month ago',
    5: 'More than a month ago',
    6: 'Never'}

readable_dict['online_frequency'] = {
    0: 'More than once a week',
    1: 'About once per week',
    2: 'Several times a month',
    3: 'About once a month',
    4: 'Once in a few months or longer',
    5: 'Never',
    999: 'Don\'t know/Prefer not to say'}

readable_dict['phone_os'] = {
    0: 'Android',
    1: 'iOS (iPhone)',
    2: 'Windows',
    3: 'Other/Not Applicable',
    4: 'Don\'t Know'}

readable_dict['iphone_version'] = {
    13: 'iPhone 13',
    12: 'iPhone 12',
    11: 'iPhone 11',
    10: 'iPhone X',
    8: 'iPhone 8',
    7: 'iPhone 7',
    6: 'Older than 7',
    99: 'Other',
    999: 'Do not know/ Prefer not to say'}

readable_dict['gender'] = {
    0: 'Male',
    1: 'Female',
    2: 'Trans Male/Trans Man',
    3: 'Trans Female/Trans Woman',
    4: 'Genderqueer/Gender Non Conforming',
    5: 'Different Identity',
    999: 'Prefer not to say'
    }

readable_dict['income'] = {
    1: 'Less than $10000',
    2: '$10000-$15999',
    3: '$16000-$19999',
    4: '$20000-$29999',
    5: '$30000-$39999',
    6: '$40000-$49999',
    7: '$50000-$59999',
    8: '$60000-$69999',
    9: '$70000-$79999',
    10: '$80000-$89999',
    11: '$90000-$99999',
    12: '$100000-$149999',
    13: 'More than $150000',
    999: 'Prefer not to say'
    }

def readable_field(fieldname, num_str):
    try:
        num = int(num_str)
    except ValueError:
        return 'NaN'
    
    field_dict = readable_dict.get(fieldname, {})
    text = field_dict.get(num, '')

    return f"{num} {text}"

retrievable_keys = ['AssignmentId','WorkerId','HITId','SubmitTime','AcceptTime']
def get_results_from_hit(HITIds, resulting_file, sandbox=False):
    fieldnames = None
    res = []
    client = get_client(sandbox=sandbox)

    for hit_id in HITIds or []:
        token = ' '
        params = dict(HITId=hit_id)
        while token:
            if token and len(token) > 1:
                params.update(dict(NextToken=token))
            resp = client.list_assignments_for_hit(**params)

            token = resp.get('NextToken')
            assignments = resp.get('Assignments')

            for i in assignments:
                answer = get_answer(i.get('Answer'))

                assignment_extra_data ={j:i.get(j) for j in retrievable_keys }

                answer.update(assignment_extra_data)
                res.append(answer)

    if False:
        if len(res) > 0:
            fieldnames = []
            for i in res:
                fieldnames.extend(i.keys())
    
            fieldnames = list(set(fieldnames))
    
        with open(resulting_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    
        with open(resulting_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for i in res:
                print(i)
                writer.writerow(i)

    df = pd.DataFrame(res)
    columns = df.columns

    # Create new columns to make data more readable
    
    if 'age' in columns:
        df['age2'] = df.apply(lambda row: age_to_generation(row['age']), axis=1)

    for column in ['shopping_device', 'date_last_purchase', 'online_frequency', 'phone_os', 'iphone_version',
                   'gender', 'income']:
        if column in columns:
            new_column = f"{column}2"
            df[new_column] = df.apply(lambda row: readable_field(column, row[column]), axis=1)
        
    df.to_csv(resulting_file, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get the results from a HIT.')

    parser.add_argument('--hit_id', dest='hit_id', action='append', help='HIT ID of HIT (can be multiple)', required=True)
    parser.add_argument('--output', dest='output', help='Output file', required=True)
    parser.add_argument('--sandbox', dest='sandbox', action='store_true', help='Whether to use the sandbox')

    args = parser.parse_args()
    
    get_results_from_hit(args.hit_id, args.output, sandbox=args.sandbox)
