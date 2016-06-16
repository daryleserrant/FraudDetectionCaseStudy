from flask import Flask, render_template, request, redirect
import cPickle as pickle
import requests
import socket
import time
from datetime import datetime

app = Flask(__name__)

# with open('data/FILENAME.pkl') as f:
#     model = pickle.load(f)

SERVER_IP = '10.3.35.182'
PORT = 5352
DATA = []
TIMESTAMP = []

REG_URL = 'http://' + SERVER_IP + '/register:5000'

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/score', methods=['POST'])
def fraud_detection_score():

    # #the following is a test 'POST' for the form found on events.html
    # text = [str(request.form['fd_form'])]
    # trans_text = model.transform(text)
    # predict = model.predict(trans_text)
    # return render_template('score.html' , text=text, predict=predict)

    DATA.append(json.dumps(request.json, sort_keys=True, indent=4, separators=(',', ': ')))
    TIMESTAMP.append(time.time())
    return DATA, TIMESTAMP

def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REG_URL, data=registration_data)


if __name__ == '__main__':
    #register for pinging service
    ip_address = socket.gethostbyname(socket.gethostname())
    print "attempting to register %s:%d" % (ip_address, PORT)
    register_for_ping(ip_address, str(PORT))

    #run app
    app.run(host='0.0.0.0', port=5000, debug=True)
