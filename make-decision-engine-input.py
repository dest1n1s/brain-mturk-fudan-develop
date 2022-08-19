import argparse

import pandas as pd

def make_decision_engine_input(files, output, columns, primary=None, sheet=None):
    dfs = []
    for file in files:
        df = pd.read_excel(file, sheet_name=sheet, engine='openpyxl')

        for colidx, column in enumerate(columns):
            if column in df.columns:
                cols = []
                cols2 = []
                cols3 = []
                if primary and primary in df.columns:
                    cols.append(primary)
                    cols2.append('primary')
                    cols3.append('primary')
                cols.append(column)
                dfsub = df[cols]
                dfsubcopy = dfsub.copy()
                dfsubcopy['colidx'] = colidx
                if primary and primary in df.columns:
                    dfsubcopy['primary'] = dfsubcopy[primary]
                dfsubcopy['text'] = dfsubcopy[column]
                cols2.append('colidx')
                cols3.append('colidx')
                cols2.append('text')
                dfsubcopy = dfsubcopy[cols2]

                dfs.append(dfsubcopy)

    df_all = pd.concat(dfs)
    df_all = df_all.sort_values(cols3)

    df_all.to_excel(output, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Take an Excel and create input to batch decision engine.')

    parser.add_argument('--file', dest='file', action='append', help='Input Excel file (can be multiple)', required=True)
    parser.add_argument('--output', dest='output', help='Output Excel file', required=True)
    parser.add_argument('--column', dest='column', action='append', help='Column with text data (can be multiple)', required=True)
    parser.add_argument('--primary_column', dest='primary_column', help='Column with primary key')
    parser.add_argument('--sheet', dest='sheet', help='Sheet in input Excels', default='Sheet1')

    args = parser.parse_args()

    make_decision_engine_input(args.file, args.output, args.column, primary=args.primary_column, sheet=args.sheet)
