from pymongo import MongoClient


class DataManager(object):

    def __init__():
        self.client = MongoClient()
        self.db = client.events

    def insert_record(self, json_data, prediction):
        data = json.load(json_data)
        data['fraud'] = prediction
        result = self.db.insert_one(json.dumps(data))
        return result.acknowledge

    def create_feature_vector(self, json_data):
        data = json.load(json_data)
        has_latitude = data['venue_name'] != None

        return np.array([data['num_payouts'], data['fb_published'], data['has_analytics'], data['show_map'], data['delivery_method'], data['currency_grp'], has_latitude])
