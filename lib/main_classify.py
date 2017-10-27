import numpy as np
from .misc import manual_rate

def main_classify(postback_list, transformer, classifier):
    '''
    Make predictions on postback_list
    Input: postback_list from main_parse, transformer, classifier
        postback_list format:
            ['url_index', 'url', 'title', 'description', 'h1', 'h2']
    Output: zipped url_index, label, and title (i, label, title)
    '''
    # Extract title from result list
    index_list = [x[0] for x in postback_list]
    url_list = [x[1] for x in postback_list]
    title_list = [x[2] for x in postback_list]
    # Transform result to aggregated features for prediction
    features = np.array(list(map(transformer.get_feature, title_list)))
    # Make classifications
    pred_list = classifier.predict(features)
    # Print classification summary
    print('{} titles need to be manually labelled.'.format(
        pred_list.count(-99)))
    print('-' * 20)
    # Manual rate the uncertain titles
    sp_flag = False # If title is still unclear, flag for special process
    for i, (label, title) in enumerate(zip(pred_list, title_list)):
        if label == -99:
            m_rate = manual_rate(title, allow_sp=True)
            if m_rate == -99:
                sp_flag = True
            pred_list[i] = m_rate
    return zip(index_list, url_list, title_list, pred_list), sp_flag