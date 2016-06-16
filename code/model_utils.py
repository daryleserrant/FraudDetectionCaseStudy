from sklearn import cross_validation
from feature_utils import featurize_data
import pandas as pd
import numpy as np
import json
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


def train_logistic_regression_model(jsonfile):
    # Featurize first and split data from library
    X_train, X_test, y_train, y_test = featurize_data(jsonfile)
    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    return lr
