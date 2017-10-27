import numpy as np

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
    # Make predictions
    output = classifier.predict(features)
    return zip(index_list, output, title_list)