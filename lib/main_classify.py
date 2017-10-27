import numpy as np
from .misc import manual_rate

def main_classify(result_list, transformer, classifier):
    '''
    Make predictions on result_list
    Input: Result_list from main_parse, transformer, classifier
    Output: zipped url_index, label, and title (i, label, title)
    '''
    # Extract title from result list
    title_list = [x[2] for x in result_list]
    index_list = [x[0] for x in result_list]
    # Transform result to aggregated features for prediction
    features = np.array(list(map(transformer.get_feature, title_list)))
    # Make classifications
    pred_list = classifier.predict(features)
    # Print classification summary
    print('{} titles need to be manually labelled.'.format(
        pred_list.count(-99)))
    print('-' * 20)
    # Manual rate the uncertain titles
    for i, (label, title) in enumerate(zip(pred_list, title_list)):
        if label == -99:
            pred_list[i] = manual_rate(title)
    return zip(index_list, pred_list, title_list)