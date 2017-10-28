import json
from lib.misc import check_status

cfg = json.load(open('config.json', 'rb'))
print(check_status(cfg['DOWNLOAD_URL']))