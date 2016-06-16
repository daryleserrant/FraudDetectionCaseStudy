from sklearn import cross_validation
from feature_utils import featurize_data, oversample
import pandas as pd
import numpy as np
import json
import time
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import recall_score

class Fraud(object):

	def __init__(self):
		self.model = LogisticRegressionCV(cv=15, scoring = recall_score)
		self.fitted = None


	def fit(self, jsonfile, target=0.3):
		X, y = featurize_data(jsonfile)

		#Balance the classes
		X_oversample, y_oversample = oversample(X, y, target) 

		#Fit the model
	    self.fitted = self.model.fit(X_oversample, y_oversample)

	 def predict(self, X_test):
	 	return self.fitted.predict_proba(X_test)[:, 1]

	 	