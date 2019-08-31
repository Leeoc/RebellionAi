import keras
import pandas as pd
import numpy as np
import re

from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Embedding, LSTM, Conv1D, MaxPooling1D, Activation, Flatten, SpatialDropout1D
from keras.optimizers import SGD

from joblib import dump, load
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier, LogisticRegression
from imblearn.over_sampling import RandomOverSampler

import pkgutil
import encodings
import os
import io
import requests
from sklearn.preprocessing import LabelEncoder

clf = LogisticRegression()
DATA_PATH = "/content/political_social_media.csv"

# Data cleaning
def clean_data(input):
    data = pd.read_csv(input,encoding='mac_roman')
    data = pd.concat([df['bias'], df['text']], axis = 1)
    # Make text lower and remove punctuation
    data['text'] = data['text'].apply(lambda x: x.lower())
    data['text'] = data['text'].apply(lambda x: re.sub('[^a-zA-z0-9\s]','',x))
    # Drop NA rows 
    data.dropna()
    labelencoder = LabelEncoder()
    data['bias'] = labelencoder.fit_transform(data['bias'])
    return data

def vectorize(df):
    X = df['text']
    print(list(X))
    y = df['bias']
    tfidf_vect = TfidfVectorizer()
    X_tfidf = tfidf_vect.fit_transform(X)
    # saving the vocab of vect, so predictions can be made in webapp
    pickle.dump(tfidf_vect.vocabulary_,open("tfidf.pkl","wb"))
    return X_tfidf
    
    
def train_model(X,y):
    sampler = RandomOverSampler()
    X_resampled, y_resampled = sampler.fit_resample(X_tfidf, y)
    X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled)
    #Fit the logistic regression model
    clf = LogisticRegression(random_state=0, class_weight='balanced', solver='lbfgs', max_iter=1000)
    clf.fit(X_train, y_train)
    #Make predictions
    y_pred = clf.predict(X_test)
    print(accuracy_score(y_pred,y_test))
    dump(clf, 'model.joblib')
    


if __name__ == "__main__":
    print("Cleaning data")
    data = clean_data(DATA_PATH)
    print("Vectorizing data")
    y = data["bias"]
    X = vectorize(data)
    print("Training model")
    train_model(X,y)
    print("Finished")