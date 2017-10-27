import requests
class Submitter:
    def __init__(self, token, target_url):
        self.token = token
        self.submit_url = target_url

    def post(self, param_dict):
        '''
        param_dict should be a dict of {'url_i': score_i}
        '''
        param = param_dict.copy()
        param['token'] = self.token

        r = requests.post(url=self.submit_url, data=param)
        value = r.content.decode('utf-8')
        return r, value

if __name__ == '__main__':
    sub = Submitter(token='iOkjn2dsAl7js4iD',
        target_url = 'http://hackathon.mzsvn.com/submit.php')
    with open('training_set', 'r') as f:
        lst = f.read().split('\n')
    scores = list(map(lambda x: int(x.split(' ')[1]), lst))
    wrong_scores = list(map(lambda x: 100-x, scores))

    short_param = dict([('url{!s}'.format(i), i) for i in range(10)])
    long_param = dict([('url{!s}'.format(i), i) for i in range(1, 101)])

    perfect_param = dict([
        ('url{!s}'.format(i+1), scores[i]) for i in range(100)])
    wrong_param = dict([
        ('url{!s}'.format(i+1), wrong_scores[i]) for i in range(100)])

    # r, v = sub.post(short_param)
    # print(r, v)
    # r, v = sub.post(long_param)
    # print(r, v)
    # r, v = sub.post(perfect_param)
    # print(r, v)
    # r, v = sub.post(wrong_param)
    # print(r, v)