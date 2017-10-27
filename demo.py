import time, os, json
import pandas as pd
# Customized tools
from lib import *
def timer(phase, comp_time, output=True):
    '''
    Print out timer info, return the current timestamp
    Input:
        phase: str
        comp_time: previous timestamp to compare
    Output (if output=True):
        end timestamp
    '''
    nowtime = time.time()
    print('{} finished. Time spent: {:.2f} secs'.format(
        phase, nowtime - comp_time))
    if output:
        return nowtime

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
    manual_rater = Selenium_helper('selenium_config.json')
    # Submission
    team_token = '84ade5bb'
    input('Ready to roll. Press Enter to start')

    start = time.time()

    # #### Download URL list
    # downloader = URL_downloader(save_folder=parse_cfg['URL_SAVE_FOLDER'])
    # url_list = downloader.get_url_list(
    #     save_file=parse_cfg['URL_SAVE_FILE'],
    #     download_url=download_url,
    #     test=False)

    download_mark = timer('Downloading', start)

    #### Parse
    # Postback list (sorted by index) ==> [index, url, title, desc, h1, h2]
    # Error list (sorted by error type & index) ==> [index, url, err_type]
    # start, parse_end, postback_list, error_list = main_parse(
    #     main_parser, url_list, parse_cfg)

    with open('result_dump/test.json', 'rb') as f:
        postback_list = json.load(f)
    postback_list = sorted(postback_list, key=lambda x: x[0])

    parse_mark = timer('Parsing', download_mark)

    #### Transform & Classify
    # Transform & auto classify
    # clsy_list ==> (index, pred, title)
    clsy_list = list(main_classify(postback_list, trans, clasr))

    tc_mark = timer('Transform & Auto Classify', parse_mark)

    # Manual labelling
    if error_list: # Only runs if error item(s) exist(s)
        print('#### Start Manual Labelling ####')
        for item in error_list:
            # If URL is valid, open in browser for rating
            if item[1]:
                print('INDEX: {}, URL: {}'.format(item[0], item[1]))
                m_rate = manual_rater.rate(item[1])
                clsy_list.append((item[0], m_rate, item[2]))

        label_mark = timer('Manual Labelling', tc_mark)
    else:
        # If no manual labelling, skip this timer
        label_mark = tc_mark

    #### Submit result
    # Only take index and label to form the submission data dictionary
    result_dict = dict([(i, label) for (i, label, title) in clsy_list])
    sub = Submitter(token=team_token,
        target_url = 'http://hackathon.mzsvn.com/submit.php')
    r, value = sub.post(result_dict)
    print('Submission result:\n{}'.format(value))

    timer('Submission', label_mark, output=False)

    #### End
    manual_rater.close()
    timer('All tasks', start, output=False)