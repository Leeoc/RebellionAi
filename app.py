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
    return clf.predict_proba(X_tfidf)

app = Flask(__name__)
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

@app.route('/')
def index():
    print('done')
    text = request.args.get('input')
    prediction = predict(text)

    return str(prediction)

if __name__ == '__main__':
    app.run(debug=True)