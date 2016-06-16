import sklearn
from feature_utils import featurize_data
from sklearn import cross_validation
from feature_utils import featurize_data
import pandas as pd
import numpy as np
import json
import time
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_classification

fpr, tpr, thresholds = sklearn.metrics.roc_curve(y_test, probabilities)

def cost_benefit(tp, fp, tn, fn):
	#return np.array([[6, -3], [0, 0]])
	return np.array([[tp, fp], [tn, fn]])

	models = [RandomForestClassifier(), LogisticRegression(), GradientBoostingClassifier(), SVC(probability=True)]
	for model in models:
	    plot_profit_curve(model, model.__class__.__name__, cb, X_train, X_test, y_train, y_test)

def profit_curve(cb, predict_probas, labels):
    sorted_idx = np.argsort(predict_probas)
    combined = np.array(zip(predict_probas, labels))
    cb = np.array(cb)
    
    profits = []
    
    profit = np.sum([cb[0, 1-l] for l in labels])
    
    profits.append(profit)
    for p, l in combined[sorted_idx]:
        profit += cb[1, 1-l] - cb[0, 1-l]
        profits.append(profit)
    return profits[::-1]

def plot_profit_curve(model, label, costbenefit, X_train, X_test, y_train, y_test, normalize=False):
    model.fit(X_train, y_train)
    predictions = model.predict_proba(X_test)[:,1]
    # print type(model).__name__, predictions
    profits = profit_curve(costbenefit, predictions, y_test)
    if normalize:
        profits = np.array(profits) / float(len(y_test))
    percentages = np.linspace(0, 100, len(profits))
    max_profit = np.max(profits)
    max_perc = percentages[np.argmax(profits)]
    print type(model).__name__, max_perc, max_profit
    plt.plot(percentages, profits, label=label)
    plt.title("Profit Curve")
    plt.xlabel("Percentage of test instances (decreasing by score)")
    plt.ylabel("Profit")
