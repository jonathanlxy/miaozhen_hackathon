import json

with open('Classifier/corpus_extra.txt', 'r') as f:
    l = f.read().split('\n')
print(l)

rate2, rate3 = [], []
for i in l:
    try:
        v, r = i.split(' ')
        if int(r) == 2:
            rate2.append(v)
        if int(r) == 3:
            rate3.append(v)
    except Exception:
        print('Error. i={}'.format(i))


with open('Classifier/corpus_add2.json', 'w') as r2:
    json.dump(rate2, r2)

with open('Classifier/corpus_add3.json', 'w') as r3:
    json.dump(rate3, r3)