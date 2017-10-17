import requests
import json
from bs4 import BeautifulSoup

class Parser:
    def __init__(self, cfg_path):
        self.req_config = json.load(
            open(cfg_path, 'rb'))

    def parse(self, url):
        self.postback = requests.get(url, self.req_config)

        if not self.postback.ok:
            'Error Code {}'.format(postback.status_code)
        else:
            soup = BeautifulSoup(self.postback.content, 'lxml')
        return soup

# Debugging only
if __name__ == '__main__':
    a = Parser()
    a.parse('http://www.google.com')
