import pickle
import numpy as np
from math import ceil

class Classifier:
    def __init__(self, model_pickle):
        # Load the pickled sklearn model
        with open(model_pickle, 'rb') as f:
            self.model = pickle.load(f)

    def predict(self, X, diff_rate=0.3):
        '''
        Input: Feature np array (n_obs, n_feature)
        Output: A list of predictions
        '''
        # Initiate
        output = np.empty(len(X))
        probablity = self.model.predict_proba(X)
        # If class probability difference >= threshold (diff_rate), then classify them directly
        # Otherwise mark for manual inspection
        diff = probablity[:, 1] - probablity[:, 0]
        confident_index = abs(diff) >= diff_rate
        # Use ceil to round up negative diff (meaning prob0 > prob1) to 0
        # positive diff (prob0 < prob1) to 1
        # There is no prob0 == prob1 case because condfident_index ensures diff
        output[confident_index] = list(map(ceil, diff[confident_index]))
        # -99 => manual classify
        output[~confident_index] = -99

        return output.tolist()

if __name__ == '__main__':
    a = Classifier('Classifier/lr_model')
    o = a.predict(features)