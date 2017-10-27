import numpy as np

def manual_rate(title):
    # Print title to screen for manual rating
    # 0 = no good (0), 1 = good (100), 5 = not sure (50)
    m_rate = None
    score_dict = {'0': 0, '1': 100, '5': 50}
    while m_rate not in score_dict:
        print('TITLE: {}'.format(title))
        m_rate = input('Rate ==> ')
        if m_rate in score_dict:
            return score_dict[m_rate]
        else:
            print('!!! Invalid score !!!')

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
    result_list = classifier.predict(features)
    # Print classification summary
    print('{} titles need to be manually labelled.'.format(
        result_list.count(-99)))
    print('-' * 20)
    # Manual rate the uncertain titles
    for i, (label, title) in enumerate(zip(result_list, title_list)):
        if label == -99:
            result_list[i] = manual_rate(title)

    return zip(index_list, result_list, title_list)