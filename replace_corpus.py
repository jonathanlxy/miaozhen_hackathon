import pandas as pd
import json

corpus_df = pd.read_csv('Classifier/corpus_1027.csv').reset_index(
    drop = True)
corpus_2_list = corpus_df[corpus_df['rate'] == 2]['token'].tolist()
corpus_3_list = corpus_df[corpus_df['rate'] == 3]['token'].tolist()

with open('Classifier/new_corpus2.json', 'w') as f:
    json.dump(corpus_2_list, f)

with open('Classifier/new_corpus3.json', 'w') as f:
    json.dump(corpus_3_list, f)