from flask import Flask, render_template, request, redirect
import cPickle as pickle


app = Flask(__name__)

with open('data/FILENAME.pkl') as f:
    model = pickle.load(f)

@app.route('/home')
def index():
    return render_template('home.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/fraud-detection')
def fraud_detection():
    return render_template('fraud-detection.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
