import pandas

df = pandas.read_csv('data.csv')
df.to_json('data.json')
