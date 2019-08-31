#!flask/bin/python
from flask import Flask
from flask import request
from flask_cors import CORS
import random
from joblib import load
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import SGDClassifier, LogisticRegression
import os
import pickle, re

vocab=pickle.load(open("tfidf.pkl", "rb"))
transformer = TfidfVectorizer(vocabulary=vocab)

def predict(input_data):
    data = re.sub('[^a-zA-z0-9\s]','',input_data).lower()
    #data = data.apply(lambda x: x.lower())

    X_tfidf = transformer.fit_transform([input_data])
    clf = load('model.joblib')
    return clf.predict(X_tfidf)

app = Flask(__name__)
#!flask/bin/python
from flask import Flask
from flask import request
from flask_cors import CORS

import imager as im
import os

UPLOAD_FOLDER = 'images/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)


@app.route('/')
def index():
    return "The backend got " + request.args.get('input') \
            + " and we just sent it back!"


@app.route('/healthcheck')
def healthcheck():
    return "I'm ok!"


@app.route('/imgSize/')
def imgSize():
    url = request.args.get(('input'))
    try:
        width, height = im.getImgSizeURL(url)
        return "Width: {}, Height: {}".format(width, height)
    except:
        return "An error occured!"


# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
@app.route('/imgUpload', methods=['POST'])
def imgUpload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file found!"
        file = request.files['file']
        if file.filename == '':
            return "File not selected"
        if file and allowed_file(file.filename):
            file = request.files['file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            file.close
            return "ok"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploadFileCheck', methods=['POST'])
def uploadFileCheck():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "No file found!"
        file = request.files['file']
        if file.filename == '':
            return "File not selected"
        if file and allowed_file(file.filename):
            file = request.files['file']
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            try:
                return im.getImgSize(file)
            except:
                return "An error occured!"
                

if __name__ == '__main__':
    app.run(debug=True)


