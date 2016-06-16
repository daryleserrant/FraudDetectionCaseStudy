from flask import Flask, render_template, request, redirect
import cPickle as pickle
import requests
import socket
import time
from datetime import datetime
import json
from code.data_manager import *
from code.model_utils import Fraud

app = Flask(__name__)
data_broker = DataManager()
fraud_model = Fraud()
fraud_model.load_model('data/model.pkl')

# with open('data/FILENAME.pkl') as f:
#     model = pickle.load(f)

SERVER_IP = '10.3.35.189'
PORT = 5353
DATA = []
TIMESTAMP = []

REG_URL = 'http://' + SERVER_IP + ':5000/register'

print REG_URL
@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/score', methods=['POST', 'GET'])
def fraud_detection_score():
    if request.method == 'GET':
        return ""
    elif request.method == 'POST':
        vector = data_broker.create_feature_vector(request.json)
        prediction = fraud_model.predict_proba(vector)
        data_broker.insert_record(request.json, prediction)
        return "posted"
    #the following is a test 'POST' for the form found on events.html
    #text = [str(request.form['fd_form'])]
    # trans_text = model.transform(text)
    # predict = model.predict(trans_text)
    # return render_template('score.html', text=text)

    #DATA.append(json.dumps(request.json, sort_keys=True, indent=4, separators=(',', ': ')))
    #TIMESTAMP.append(time.time())
    #return ' '.join(DATA)


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
