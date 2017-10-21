import requests
import json
from bs4 import BeautifulSoup

def element_extract(soup):
    title = soup.title
    description = soup.find('meta', {'name': 'description'})
    h1 = soup.find('h1')
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
    def __init__(self, cfg_path=None):
        # Parser config
        if cfg_path:
            self.req_config = json.load(
                open(cfg_path, 'rb'))

    def parse(self, url):
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
            print('Postback error')
            raise PostbackError(url)

# Debugging only
if __name__ == '__main__':
    a = Parser('request_config.json')
    a.parse('http://www.google.com')
