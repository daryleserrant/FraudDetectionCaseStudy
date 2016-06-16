from sklearn import cross_validation
from feature_utils import featurize_data
import pandas as pd
import numpy as np
import json
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression


def train_logistic_regression_model(jsonfile):
	#Featurize first and split data from library

	lr = LogisticRegression()
	lr.fit(X_train, y_train)
	lr.score(X_test, y_test)
    return 
