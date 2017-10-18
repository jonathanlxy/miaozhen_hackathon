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

    return title, description, h1, h2

class Parser:
    def __init__(self, cfg_path, log_path):
        # Parser config
        self.req_config = json.load(
            open(cfg_path, 'rb'))
        # Folder to save the parsed htmls
        self.log_path = log_path

    def parse(self, url):
        # Load page
        postback = requests.get(url, self.req_config)
        # Make soup, extract elements
        if postback.ok:
            soup = BeautifulSoup(postback.content, 'lxml')
            elements = element_extract(soup)
            # Tag the extracted elements with url
            elements['url'] = url
            # Return key elements & the soup
            return elements, soup
        # If request failed, log the error
        with open(self.log_path, 'a') as f:
            f.write('{}|{}\n'.format(postback.status_code, url))

# Debugging only
if __name__ == '__main__':
    a = Parser()
    a.parse('http://www.google.com')
