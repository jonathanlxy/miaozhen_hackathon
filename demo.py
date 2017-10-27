import time, os, json, sys
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

def testing_load(postback_dump, error_log):
    # Load & make sure postback list was sorted
    postback_list = json.load(open(postback_dump, 'rb'))
    postback_list = sorted(postback_list, key=lambda x: x[0])
    # Load & make sure error list was sorted
    error_raw = json.load(open(error_log, 'rb'))
    error_0 = [i for i in error_raw if i[2] == 'PostbackError']
    error_1 = [i for i in error_raw if i[2] == 'RequestError']
    error_list = sorted(error_0 + error_1, key=lambda x: x[0])
    return postback_list, error_list

if __name__ == '__main__':
    switch = input('Select Mode (t=tesing/p=production): ')
    if switch == 't':
        prod = False
    elif switch == 'p':
        prod = True
    else:
        print(switch)
        print('Invalid input. Script abort.')
        sys.exit()

    #### Initiate
    print('Initiating...')
    cfg = json.load(open('config.json', 'rb'))
    download_url = cfg['DOWNLOAD_URL']
    team_token = cfg['TEAM_TOKEN']
    # Corpus
    corpus_df = pd.read_csv('corpus.csv').reset_index(drop = True)
    corpus_2_list = corpus_df[corpus_df['rate'] == 2]['token'].tolist()
    corpus_3_list = corpus_df[corpus_df['rate'] == 3]['token'].tolist()
    # Expose the service APIs here for debugging purpose
    downloader = URL_downloader(save_folder=cfg['URL_SAVE_FOLDER'])
    main_parser = Parser(cfg['REQUEST_CONFIG'])
    trans = Transformer(corpus_2_list, corpus_3_list)
    clasr = Classifier('Classifier/lr_model')
    sel_rater = Selenium_helper(cfg['SEL_CONFIG'])

    # Ready
    print('-' * 20)
    input('Ready to roll. Press Enter to start')

    start = time.time()

    #### Download URL list
    if prod: # Only runs in production mode
        url_list = downloader.get_url_list(
            save_file=cfg['URL_SAVE_FILE'],
            download_url=download_url,
            test=False)

    download_mark = timer('Downloading', start)

    #### Parse
    # Postback list (sorted by index) ==> [index, url, title, desc, h1, h2]
    # Error list (sorted by error type & index) ==> [index, url, err_type]
    if prod: # Only runs in production mode
        start, parse_end, postback_list, error_list = main_parse(
            main_parser, url_list, cfg)

    else: # Load saved lists in testing mode
        postback_list, error_list = testing_load(
            'postback_dump/test.json',
            'error_log/test.log')

    parse_mark = timer('Parsing', download_mark)

    #### Transform & Classify
    # Transform & auto classify
    # clsy_zip ==> (index, url, title, pred)
    clsy_zip, sp_flag = main_classify(postback_list, trans, clasr)
    clsy_list = list(clsy_zip)

    tc_mark = timer('Transform & Auto Classify', parse_mark)

    # Selenium inspection
    if sp_flag: # If main_classify returns positive sp_flag,
    # add the sp results for inspection
        sp_list = []
        for (i, url, title, label) in clsy_list:
            if label == -99:
                sp_list.append([i, url, 'Unclear Title'])
        error_list = sp_list + error_list

    if error_list: # Only runs if error item(s) exist(s)
        print('#### Start Selenium Inspection ####')
        for i, url, err_type in error_list:
            # If URL is valid, open in browser for rating
            if url:
                print('INDEX: {}, URL: {}'.format(i, url))
                m_rate = sel_rater.rate(url)
                clsy_list.append((i, url, err_type, m_rate))

        label_mark = timer('Selenium inspection', tc_mark)
    else:
        # If no manual labelling, skip this timer
        label_mark = tc_mark

    #### Submit result
    # Only take index and label to form the submission data dictionary
    result_dict = dict([(i, label) for (i, url, title, label) in clsy_list])
    sub = Submitter(token=team_token,
        target_url = 'http://hackathon.mzsvn.com/submit.php')
    r, value = sub.post(result_dict)
    print('Submission result:\n{}'.format(value))

    timer('Submission', label_mark, output=False)

    #### Dump Classification Results as csv
    #### Construct result dataset
    cols = ['url_index', 'url', 'title', 'label']
    result_df = pd.DataFrame(clsy_list, columns = cols)
    result_df.to_csv(cfg['RESULT_DUMP'], index=False)

    #### End
    sel_rater.close()
    timer('All tasks', start, output=False)