import time, os, json
# Have to mark the time here to cover (almost) all of the imports
start = time.time()
import pandas as pd
# Customized tools
from lib import *


# TODO: Take external arg to point parser log path, save path, etc
if __name__ == '__main__':
    #### Initiate
    # Expose the service APIs here for debugging purpose
    print('Initiating...')
    # Parse
    download_url = 'http://hackathon.mzsvn.com/download.php'
    parse_cfg = json.load(open('parser_config.json', 'rb'))
    main_parser = Parser(parse_cfg['REQUEST_CONFIG'])
    # Transform & Classify
    corpus_df = pd.read_csv('corpus.csv').reset_index(drop = True)
    corpus_2_list = corpus_df[corpus_df['rate'] == 2]['token'].tolist()
    corpus_3_list = corpus_df[corpus_df['rate'] == 3]['token'].tolist()
    trans = Transformer(corpus_2_list, corpus_3_list)
    clasr = Classifier('Classifier/lr_model')
    # manual_rater = Selenium_helper('selenium_config.json')
    print('Ready. Time spent: {}'.format(time.time() - start))
    input('Press Enter to start')

    # #### Download URL list
    # downloader = URL_downloader(save_folder=parse_cfg['URL_SAVE_FOLDER'])
    # url_list = downloader.get_url_list(
    #     save_file=parse_cfg['URL_SAVE_FILE'],
    #     download_url=download_url,
    #     test=False)

    # #### Parse - returned result & error lists will be sorted already
    # start, parse_end, result_list, error_list = main_parse(
    #     main_parser, url_list, parse_cfg)

    with open('result_dump/test.json', 'rb') as f:
        result_list = json.load(f)
    result_list = sorted(result_list, key=lambda x: x[0])

    #### Transform & Classify

    clsy_result = list(main_classify(result_list, trans, clasr))
    for i, t in enumerate(clsy_result):
        if np.array_equal(trans.get_feature(t[2]), np.array([0, 1, 0, 0])):
            print(t[2])
            print(trans.get_feature(t[2]), t[1])
            input()

    #### Construct result dataset
    # element_cols = ['url_index', 'url', 'title',
    #                 'description', 'h1', 'h2']
    # result_df = pd.DataFrame(result_list, columns = element_cols)


    # print('Result DF finished. Time spent: {:.2f}'.format(
    #     end - parse_end))
    # print('#'*20)
    #### Submit result
    # sub = Submitter(token='iOkjn2dsAl7js4iD',
    #     target_url = 'http://hackathon.mzsvn.com/submit.php')
    # r, value = sub.post(result_dict)
    # print('Submission result:\n{}'.format(value))
    # #### End
    # print('Job done. Total execution Time: {:.2f} secs'.format(
    #     time.time() - start))

    ## Selenium
    # 1. open Postback Error
    # 2. open Request Error
    # manual_rater.close()
    ## If some url left unrated & in error list, classify as 0