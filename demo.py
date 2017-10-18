from task_handlers import URL_downloader
from Parser import Parser
import pandas as pd

# TODO: Take external arg to point parser log path, save path, etc
# Initiate tools
parser = Parser('request_config.json', 'parser_log/test.log')
downloader = URL_downloader('URL_lists')

# Load URL list
url_list = downloader.get_url_list('test_list')

# TODO: try parser and see if the df.append can handle NoneType

'''
# Result dataset
element_cols = ['url_index', 'title', 'description',
                'h1', 'h2', 'url']
## Result collection
df = pd.DataFrame(columns=element_cols)

# Parse key elements from each URL
for i, url in enumerate(url_list):

    if i > 2: break # Test

    # Load URL
    result = parser.parse(url)
    # In case parse failed, pass to next iteration
    # Error message logged.
    if not result:
        continue

    # Get elements & soup
    elements, soup = result
    # Dump soup
    with open('parsed_pages/test/{}.html'.format(i), 'w') as page:
        page.write(soup.prettify('utf-8'))
    # Append the elements to dataset
    new_row = [i] + elements + [url]
    df.append(new_row, ignore_index = True)
'''