from lib import URL_downloader, Parser
import pandas as pd
import time

# TODO: Take external arg to point parser log path, save path, etc
# Initiate tools
parser = Parser('request_config.json', 'parser_log/test.log')
downloader = URL_downloader('URL_lists')

# Load URL list
url_list = downloader.get_url_list('test_list')

## Result collection
result_list = []
error_list = [] # Catch the unexpected error during parsing

# Parse key elements from each URL
time1 = time.time()
for i, url in enumerate(url_list):
    # if i > 10: break # Test
    print('Parsing URL {}'.format(i))

    ### Error handling
    try:
        result = parser.parse(url)
    # In case parse failed, pass to next iteration
    # Error message logged.
    except Exception as err:
        error_list.append((i, url, err))
        continue
    # If parser catches & logs error, move to next URL
    if not result:
        continue

    # Get elements & soup
    elements, soup = result
    # Dump soup
    with open('parsed_pages/test/{}.html'.format(i), 'wb') as page:
        page.write(soup.prettify('utf-8'))
    # Append the elements to dataset
    new_row = [i, url] + elements
    result_list.append(new_row)

print('Execution Time: {} secs'.format(time.time() - time1))

# Result dataset
element_cols = ['url_index', 'url', 'title',
                'description', 'h1', 'h2']
result_df = pd.DataFrame(result_list, columns = element_cols)