import argparse
import datetime
import json
import os
import requests

import pandas as pd
from tqdm import tqdm

tqdm.pandas()

parser = argparse.ArgumentParser(description='Add reasons to metrics output Excel file.')

parser.add_argument('--input', dest='input', help='input Excel file', required=True)
parser.add_argument('--output', dest='output', help='output Excel file', default='out.xlsx')
parser.add_argument('--head', dest='head', type=int, help='How many of the first N to use')
parser.add_argument('--staging', dest='staging', action='store_true', help='Use the staging version of natural_reasons')
parser.add_argument('--unique_texts', dest='unique_texts', action='store_true', help='Remove duplicate texts.')

args = parser.parse_args()

if args.staging:
    url = 'https://api-dev.braininc.net/be/bas-demo-v4/nlp/domain_mapping'
    token = os.getenv('BRUS_AUTH_TOKEN_STAGING')
else:
    url = 'https://api.braininc.net/be/bas-demo-v4/nlp/domain_mapping'
    token = os.getenv('BRUS_AUTH_TOKEN')

headers = {
    'Authorization': f"Token {token}",
    'Content-Type': 'application/json'
}

# Function to hit domain mapping

def get_reasons(text):

    specified_intents = []
    statuses = []
    nlp_session_ids = []
    secondss = []
    intents = []
    reasons = []
    angles = []

    body = {
        'text': text,
        'decision_engine': 'true'
    }

    before = datetime.datetime.now()
    r = requests.post(url, data=json.dumps(body), headers=headers)
    status = r.status_code
    end = datetime.datetime.now()
    diff = end - before
    seconds = diff.total_seconds()

    if status == 200:
        rbody = r.json()
        nlp_session_id = rbody.get('nlp_session_id', '')
        results = rbody.get('results', [])

        if len(results) > 1:
            # We have multiple action_ids; re-run

            for result in results:
                intent_arr = result.get('action_ids', [None])
                intent = intent_arr[0]

                body = {
                    'text': text,
                    'decision_engine': 'true',
                    'action_id': intent
                }

                before = datetime.datetime.now()
                r2 = requests.post(url, data=json.dumps(body), headers=headers)
                status2 = r2.status_code
                end = datetime.datetime.now()
                diff = end - before
                seconds2 = diff.total_seconds()

                specified_intents.append(True)
                statuses.append(status2)
                secondss.append(seconds2)
                intents.append(intent)
                if status2 == 200:
                    rbody2 = r2.json()
                    nlp_session_id2 = rbody2.get('nlp_session_id', '')
                    nlp_session_ids.append(nlp_session_id2)
                    results2 = rbody2.get('results', [])
                    result2 = results2[0]
                    if 'decision_engine' in result2:
                        de2 = result2.get('decision_engine', {})
                        reasons.append(de2.get('reasons', []))
                        angles.append(de2.get('angles', []))
                    else:
                        reasons.append([])
                        angles.append([])
                else:
                    nlp_session_ids.append('')
                    secondss.append(-1)
                    specified_intents.append(True)
                    intents.append(intent)
                    reasons.append([])
                    angles.append([])
        else:
            # Only one intent; no need to re-run
            result = results[0]
            specified_intents.append(False)
            statuses.append(status)
            secondss.append(seconds)
            nlp_session_ids.append(nlp_session_id)
            intent_arr = result.get('action_ids', [None])
            intent = intent_arr[0]
            intents.append(intent)
            if 'decision_engine' in result:
                de = result.get('decision_engine', {})
                reasons.append(de.get('reasons', []))
                angles.append(de.get('angles', []))
            else:
                reasons.append([])
                angles.append([])
    else:
        statuses.append(status)
        nlp_session_ids.append('')
        secondss.append(-1)
        specified_intents.append(False)
        intents.append([])
        reasons.append([])
        angles.append([])

    return (json.dumps(specified_intents),
            json.dumps(statuses),
            json.dumps(nlp_session_ids),
            json.dumps(secondss),
            json.dumps(intents),
            json.dumps(reasons),
            json.dumps(angles))


input_df = pd.read_excel(args.input, engine='openpyxl')

df = input_df

# Remove duplicate texts
if args.unique_texts:
    df = df.drop_duplicates(subset=['text'])

# Overall head
if args.head:
    df = df.head(args.head)

# Hit domain mapping

df['reasons_raw'] = df.progress_apply(lambda row: get_reasons(row['text']), axis=1)

# Expand reasons

if 'primary' in df.columns:
    primary_idx = df.columns.get_loc('primary') + 1
else:
    primary_idx = None

text_idx = df.columns.get_loc('text') + 1
colidx_idx = df.columns.get_loc('colidx') + 1
reasons_raw_idx = df.columns.get_loc('reasons_raw') + 1

all_reasons = []
api_idx = 0
for i in df.itertuples():
    if primary_idx:
        primary = i[primary_idx]
    else:
        primary = None

    text = i[text_idx]
    colidx = i[colidx_idx]
    reasons_raw = i[reasons_raw_idx]

    specified_intents = json.loads(reasons_raw[0])
    statuss = json.loads(reasons_raw[1])
    nlp_session_ids = json.loads(reasons_raw[2])
    secondss = json.loads(reasons_raw[3])
    intents = json.loads(reasons_raw[4])
    reasonss = json.loads(reasons_raw[5])
    angless = json.loads(reasons_raw[6])

    for idx, status in enumerate(statuss):
        specified_intent = specified_intents[idx]
        nlp_session_id = nlp_session_ids[idx]
        seconds = secondss[idx]
        intent = intents[idx]
        reasons = reasonss[idx]
        angles = angless[idx]

        if status == 200:
            if len(reasons) > 0:
                for ridx, reason in enumerate(reasons):
                    row = []

                    if primary:
                        row.append(primary)
                    row.append(colidx)
                    row.append(api_idx)
                    row.append(text)
                    row.append(specified_intent)
                    row.append(status)
                    row.append(nlp_session_id)
                    row.append(seconds)
                    row.append(intent)
                    row.append('reason')
                    row.append(ridx)
                    row.append(reason)

                    all_reasons.append(row)
            else:
                row = []

                if primary:
                    row.append(primary)
                row.append(colidx)
                row.append(api_idx)
                row.append(text)
                row.append(specified_intent)
                row.append(status)
                row.append(nlp_session_id)
                row.append(seconds)
                row.append(intent)
                row.append('reason')
                row.append(-1)
                row.append('')

                all_reasons.append(row)

            if len(angles) > 0:
                for aidx, angle in enumerate(angles):
                    row = []

                    if primary:
                        row.append(primary)
                    row.append(colidx)
                    row.append(api_idx)
                    row.append(text)
                    row.append(specified_intent)
                    row.append(status)
                    row.append(nlp_session_id)
                    row.append(seconds)
                    row.append(intent)
                    row.append('angle')
                    row.append(aidx)
                    row.append(angle)

                    all_reasons.append(row)
            else:
                row = []

                if primary:
                    row.append(primary)
                row.append(colidx)
                row.append(api_idx)
                row.append(text)
                row.append(specified_intent)
                row.append(status)
                row.append(nlp_session_id)
                row.append(seconds)
                row.append(intent)
                row.append('angle')
                row.append(-1)
                row.append('')

                all_reasons.append(row)
        else:
            row = []

            if primary:
                row.append(primary)
            row.append(colidx)
            row.append(api_idx)
            row.append(text)
            row.append(specified_intent)
            row.append(status)
            row.append(nlp_session_id)
            row.append(seconds)
            row.append('')
            row.append('status not 200')
            row.append(-1)
            row.append('')

            all_reasons.append(row)
    api_idx += 1

# Create dataframe

out_columns = []
if primary_idx:
    out_columns.append('primary')
out_columns.append('colidx')
out_columns.append('api_idx')
out_columns.append('text')
out_columns.append('specified_intent')
out_columns.append('status')
out_columns.append('nlp_session_id')
out_columns.append('seconds')
out_columns.append('intent')
out_columns.append('type')
out_columns.append('reason_num')
out_columns.append('reason/angle')

df_reasons = pd.DataFrame(all_reasons, columns=out_columns)

# Dump file

df_reasons.to_excel(args.output, index=False)
