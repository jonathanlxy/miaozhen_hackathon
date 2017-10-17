from task_dispenser import URL_downloader
from Parser import Parser

parser = Parser('request_config.json')
downloader = URL_downloader('URL_lists')

# Load URL list
url_list = downloader.get_url_list('test_list')

# Try parse a webpage
url = url_list.pop()

soup = parser.parse(url)