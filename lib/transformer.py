import numpy as np
from synonyms import nearby
from jieba import cut_for_search, add_word
from zhconv import convert

class Transformer:
    def __init__(self, corpus_rate2, corpus_rate3,
        corpus_add2=[], corpus_add3=[]):
        '''
        corpus_rateX are lists that contains corresponding tokens
        '''
        self.corpus2 = corpus_rate2 + corpus_add2
        self.corpus3 = corpus_rate3 + corpus_add3
        for token in corpus_rate2 + corpus_rate3:
            add_word(token)

    def tokenize(self, doc):
        # Remove duplicates & force to lower case
        return set(cut_for_search(convert(doc.lower(), 'zh-cn')))

    def rate_token(self, token):
        '''
        Input: A single token
        Output: A rate based on token itself
        '''
        if token in self.corpus3:
            return 3
        elif token in self.corpus2:
            return 2
        else:
            return 0

    def rate_synonym(self, token):
        '''
        Input: A single token
        Output: A rate based on token's synonyms
        '''
        # Get the synonyms of the token
        synonyms = nearby(token)[0]
        # Count rate 2 and 3
        scores_agg = list(map(self.rate_token, synonyms))
        score_2, score_3 = scores_agg.count(2), scores_agg.count(3)
        # If no match, return 0, else 3 has higher weight than 2
        if score_3 == score_2 == 0:
            return 0
        elif score_3 < score_2:
            return 2
        else:
            return 3

    def get_feature(self, doc):
        '''
        Extract token rate features from a single document
        Input: A single string
        Output: A numpy array that contains 4 elements
            [token_2, token_3, synonym_2, synonym_3]
        '''
        # Tokenize document for rating
        tokens = self.tokenize(doc)

        # Rating temp list, same length
        token_rate_list = [0] * len(tokens)
        synonym_rate_list = token_rate_list.copy()

        # Rate each token in the doc
        for i, tok in enumerate(tokens):
            # Rate the token
            token_rate = self.rate_token(tok)
            if not token_rate:
                # If no match on token itself, get the synonym rate
                synonym_rate_list[i] = self.rate_synonym(tok)
            else:
                # If match(es) found, skip the synonym rating
                token_rate_list[i] = token_rate

        # Aggregate features
        feature = np.array([token_rate_list.count(2), token_rate_list.count(3),
                            synonym_rate_list.count(2), synonym_rate_list.count(3)])

        return feature

if __name__ == '__main__':
    import pandas as pd
    corpus_df = pd.read_csv('Classifier/corpus_1027.csv').reset_index(
        drop = True)
    corpus_2_list = corpus_df[corpus_df['rate'] == 2]['token'].tolist()
    corpus_3_list = corpus_df[corpus_df['rate'] == 3]['token'].tolist()
    a = Transformer(corpus_2_list, corpus_3_list)
    t1 = '小女生'
    t2 = '小女孩'
    s1 = '把衣服全脱了'
    s2 = '把衣服全脱光'
    w1 = '舆情分析：兰陵一副校长致初中女生"怀孕"'
    w2 = '写代码容易吗，放松一下吧，苍老师的高清片子'
    w3 = '《同意》“把衣服全脱了，不要问我任何问题”'
    for s in [t1, t2, s1, s2, w1, w2, w3]:
        print('String: {}'.format(s))
        print('Token: {}'.format(a.tokenize(s)))
        print('Feature: {}'.format(a.get_feature(s)))