import json
import requests

def check_status(download_url):
    postback = requests.get(download_url)
    if postback.ok:
        print(postback.content)
    else:
        print('Error.')

cfg = json.load(open('config.json', 'rb'))
print(check_status(cfg['DOWNLOAD_URL']))