from pymongo import MongoClient
import json
import numpy as np

class DataManager(object):

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.fraud
        self.coll = self.db.events

    def insert_record(self, json_data, prediction):
        json_data['fraud'] = 1 if prediction == 1 else 0
        result = self.coll.insert_one(json_data)

    def create_feature_vector(self, json_data):
        currency_grp = json_data['currency'] in ('GBP', 'USD', 'EUR', 'CAD')
        has_latitude = json_data['venue_name'] != None

        return np.array([json_data['num_payouts'], json_data['fb_published'], json_data['has_analytics'], json_data['show_map'], json_data['delivery_method'], currency_grp, has_latitude])
