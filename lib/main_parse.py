from multiprocessing import Process, Queue, Pool
import time, os
from lib.parser import Parser, RequestError, PostbackError
from lib.misc import result_dump

def parse_init(parser, result_q, error_q, save_folder):
    # This is a monkey patch, which allows us to modify the
    # attributes in run time. Also, methods in python are also objects,
    # which allows this f.q operation
    # https://stackoverflow.com/questions/3827065/can-i-use-a-multiprocessing-queue-in-a-function-called-by-pool-imap
    parse.parser = parser
    parse.result_q = result_q
    parse.error_q = error_q
    parse.save_folder = save_folder

def parse(i, url):
    taskid = os.getpid()
    print('Task {} Parsing URL {}'.format(taskid, i))
    #### Error handling
    try:
        result = parse.parser.parse(url)
    # In case parse failed, pass to next iteration
    # Error message logged.
    except (RequestError, PostbackError) as err:
        # type(err).__name__ gets error type, err it self contains the message
        err_type = type(err).__name__
        print('{} while parsing URL {}'.format(err_type, i))
        parse.error_q.put((i, url, err_type, err))
        return None
    #### Get elements & soup
    elements, soup = result
    # Dump soup
    with open('{}/{}.html'.format(parse.save_folder, i), 'wb') as page:
        page.write(soup.prettify('utf-8'))
    # Append the elements to dataset
    new_row = [i, url] + elements
    parse.result_q.put(new_row)

def main_parse(parser, url_list, cfg):
    #### Download URL list
    # Timing point 1
    start = time.time()
    print('Script starts. Downloading URL list.')

    # Timing point 2
    url_end = time.time()
    print('URL list downloaded. Time spent: {:.2f}'.format(
        url_end - start))
    print('#'*20)

    #### Parallel parsing
    print('Start parsing.')
    result_q = Queue() # Store the parsing results
    error_q = Queue() # Catch the error during parsing
    # Parse key elements from each URL
    with Pool(processes=4, initializer=parse_init,
        initargs=[parser, result_q, error_q, cfg['PARSER_SAVE_FOLDER']]) as p:
        p.starmap(parse, enumerate(url_list))
    # Collect results
    n_result, n_error = result_q.qsize(), error_q.qsize()
    postback_list = sorted([result_q.get() for i in range(n_result)],
        key=lambda x: x[0])
    error_raw = [error_q.get() for i in range(n_error)]
    if error_raw: # Sort error list by error_type then url index
        error_0 = [i for i in error_raw if i[2] == 'PostbackError']
        error_1 = [i for i in error_raw if i[2] == 'RequestError']
        error_list = sorted(error_0 + error_1, key=lambda x: x[0])

    # Timing point 3
    parse_end = time.time()
    print('Parse finish. Time spent: {:.2f}'.format(parse_end - url_end))
    print('Results: {}. Error: {}'.format(n_result, n_error))
    print('#'*20)

    #### Dump result
    try:
        if n_error:
            result_dump(error_list, cfg['ERROR_LOG'])
        else:
            print('No error occurred')
        if n_result:
            result_dump(postback_list, cfg['POSTBACK_DUMP'])
        else:
            print('!!!!! No postback !!!!!')
    except:
        print('Error dumping error & postback')
        pass
    end = time.time()

    return start, end, postback_list, error_list