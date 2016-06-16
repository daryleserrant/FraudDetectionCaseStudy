from flask import Flask, render_template, request, redirect
import cPickle as pickle
import requests
import socket
import time
from datetime import datetime
import json
from src.data_manager import DataManager
from src.model_utils import Fraud

app = Flask(__name__)
data_broker = DataManager()
fraud_model = Fraud()
fraud_model.load_model('data/model.pkl')

SERVER_IP = '10.3.35.189'
PORT = 5353

REG_URL = 'http://' + SERVER_IP + ':5000/register'

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/score', methods=['POST', 'GET'])
def fraud_detection_score():
    if request.method == 'GET':
        return ""
    elif request.method == 'POST':
        # print type(request.json)
        # print json.dump(request.json)
        vector = data_broker.create_feature_vector(request.json)
        prediction = fraud_model.predict(vector)
        data_broker.insert_record(request.json, prediction)
        return "predicted" # "This event is <h1>{}</h1>!".format(prediction)


def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REG_URL, data=registration_data)


if __name__ == '__main__':
    # register for pinging service
    ip_address = socket.gethostbyname(socket.gethostname())
    print "local", ip_address
    print "attempting to register %s:%d" % (ip_address, PORT)
    register_for_ping(ip_address, str(PORT))

    # run app
    app.run(host='0.0.0.0', port=5353, debug=True)
