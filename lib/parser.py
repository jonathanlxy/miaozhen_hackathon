import requests
import json
from bs4 import BeautifulSoup

def element_extract(soup):
    title = soup.title
    description = soup.find('meta', {'name': 'description'})
    h1 = soup.h1
    h2 = soup.h2

    if title:
        title = title.text
    if description:
        description = description['content']
    if h1:
        h1 = h1.text
    if h2:
        h2 = h2.text

    return [title, description, h1, h2]

class RequestError(Exception):
    # Used to flag request fail (e.g. Timeout)
    pass

class PostbackError(Exception):
    # Used when requests.get() returns error code (e.g. 404)
    pass

class Parser:
    def __init__(self, cfg=None):
        # Parser config
        if cfg:
            self.req_config = cfg

    def parse(self, url, force_postback=False):
        # Load page
        try:
            postback = requests.get(url, **self.req_config)
        except: # If request failed, log the request fail.
            print('Request error')
            raise RequestError(url)
        # Make soup, extract elements
        if postback.ok:
            soup = BeautifulSoup(postback.content, 'lxml')
            elements = element_extract(soup)
            # Return key elements & the soup
            return elements, soup
        else: # If postback failed, log the status code.
            print('Postback error: {}'.format(postback.status_code))
            if force_postback:
                return postback
            else:
                raise PostbackError(postback.status_code)

# Debugging only
if __name__ == '__main__':
    cfg = {
        "timeout": 4,
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
            "Accept": "application/json, text/javascript"
        }
    }
    a = Parser(cfg)
    res = a.parse('http://www.dianping.com/shop/27215019',
        force_postback=True)
