import pandas as pd

df = pd.read_csv('./train-sample.csv')

df = df.fillna("")

def iteration(dfpart):
    for body in dfpart.iterrows():
        print(body)
        raw_input('Press Enter for next Question')

iteration(df[df.OpenStatus == 'open']['BodyMarkdown'])
