import pandas as pd

kosong = pd.DataFrame(columns=df.columns)

panjangKolom = len(df['c1'])
x=0
while x < panjangKolom:
    kosong.at[x, 'c1'] = df.at[x, 'c1'] / df['c1'].max()
    x += 1

kosong.head()

