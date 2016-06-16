from sklearn import cross_validation
from feature_utils import featurize_data, oversample
import pandas as pd
import numpy as np
import json
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import recall_score
import cPickle as pickle


class Fraud(object):
    def __init__(self):
        self.model = None
        self.fitted = False

    def fit(self, jsonfile, target=0.3):
        self.model = LogisticRegressionCV(cv=15, scoring='recall')
        X, y = featurize_data(jsonfile)

        # Balance the classes
        X_oversample, y_oversample = oversample(X, y, target)
        print X_oversample, y_oversample

        # Fit the model
        self.model.fit(X_oversample, y_oversample)
        self.fitted = True

    def predict(self, X_test):
        return self.model.predict(X_test)[0]

    def save_model(self, picklefile):
        with open(picklefile, 'w') as f:
            pickle.dump(self.model, f)

    def load_model(self, picklefile):
        with open(picklefile, 'r') as f:
            self.model = pickle.load(f)
            self.fitted = True

if __name__ == '__main__':
    fraud = Fraud()
    fraud.fit('../data/train_new.json')
    fraud.save_model('../data/model.pkl')
