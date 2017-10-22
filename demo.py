from multiprocessing import Process, Queue, Pool
import pandas as pd
import time, os
# Customized tools
from lib import *

# TODO: Take external arg to point parser log path, save path, etc
def main_init(parser, result_q, error_q, save_path):
    # This is a monkey patch, which allows us to modify the
    # attributes in run time. Also, methods in python are also objects,
    # which allows this f.q operation
    # https://stackoverflow.com/questions/3827065/can-i-use-a-multiprocessing-queue-in-a-function-called-by-pool-imap
    main.parser = parser
    main.result_q = result_q
    main.error_q = error_q
    main.save_path = save_path

def main(i, url):
    taskid = os.getpid()
    print('Task {} Parsing URL {}'.format(taskid, i))
    #### Error handling
    try:
        result = parser.parse(url)
    # In case parse failed, pass to next iteration
    # Error message logged.
    except (RequestError, PostbackError) as err:
        print('{} while parsing URL {}'.format(err , i))
        main.error_q.put((i, url, err))
        return None
    #### Get elements & soup
    elements, soup = result
    # Dump soup
    with open('{}/{}.html'.format(main.save_path, i), 'wb') as page:
        page.write(soup.prettify('utf-8'))
    # Append the elements to dataset
    new_row = [i, url] + elements
    main.result_q.put(new_row)

def result_dump(result_list, path):
    with open(path, 'w') as f:
        for res in result_list:
            f.write('{}\n'.format(result_list))

def
if __name__ == '__main__':
    #### Initiate
    config = json.load(open('parser_config.json', 'rb'))

    #### Download URL list
    # Timing point 1
    start = time.time()
    print('Script starts. Downloading URL list.')
    # Download
    downloader = URL_downloader(save_folder=config['URL_SAVE_FOLDER'])
    url_list = downloader.get_url_list(
        save_file=config['URL_SAVE_FILE'], test=True)
    # Timing point 2
    url_end = time.time()
    print('URL list downloaded. Time spent: {:.2f}'.format(
        url_end - start))
    print('#'*20)

    #### Parallel parsing
    print('Start parsing.')
    parser = Parser(config['PARSER_CONFIG'])
    result_q = Queue() # Store the parsing results
    error_q = Queue() # Catch the error during parsing
    # Parse key elements from each URL
    with Pool(processes=4, initializer=main_init,
        initargs=[parser, result_q, error_q, config['URL_SAVE_FILE']]) as p:
        p.starmap(main, enumerate(url_list))
    # Collect results
    n_result, n_error = result_q.qsize(), error_q.qsize()
    result_list = [result_q.get() for i in range(n_result)]
    error_list = [error_q.get() for i in range(n_error)]
    # Timing point 3
    parse_end = time.time()
    print('Parse finish. Time spent: {:.2f}'.format(parse_end - url_end))
    print('Results: {}. Error: {}'.format(n_result, n_error))
    print('#'*20)

    #### Dump result
    result_dump(error_list, config['ERROR_LOG'])
    result_dump(result_list, config['RESULT_DUMP'])

    # #### Construct result dataset
    # element_cols = ['url_index', 'url', 'title',
    #                 'description', 'h1', 'h2']
    # result_df = pd.DataFrame(result_list, columns = element_cols)
    # end = time.time()
    # print('Result DF finished. Time spent: {:.2f}'.format(
    #     end - parse_end))
    # print('#'*20)
    print('Job done. Total execution Time: {:.2f} secs'.format(
        end - start))