from flask import Flask, render_template, request, url_for, Markup, jsonify
import pickle
import pandas as pd
import numpy as np
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.util import ngrams
from nltk.tokenize import word_tokenize
# nltk.download('punkt')

table = str.maketrans({key: None for key in string.punctuation})
cls = pickle.load(open('classifierx.pickle', 'rb'))


featureDict = {} # A global dictionary of features

def toFeatureVector(Rating, verified_Purchase, product_Category, tokens):
    localDict = {}
    
    #Labels

    # featureDict["L"] = 1   
    # localDict["L"] = labels
    featureDict["R"] = 1   
    localDict["R"] = Rating


    #Verified_Purchase
  
    featureDict["VP"] = 1
            
    if verified_Purchase == "N":
        localDict["VP"] = 0
    else:
        localDict["VP"] = 1

    #Product_Category

    
    if product_Category not in featureDict:
        featureDict[product_Category] = 1
    else:
        featureDict[product_Category] = +1
            
    if product_Category not in localDict:
        localDict[product_Category] = 1
    else:
        localDict[product_Category] = +1
            
            
    #Text        

    for token in tokens:
        if token not in featureDict:
            featureDict[token] = 1
        else:
            featureDict[token] = +1
            
        if token not in localDict:
            localDict[token] = 1
        else:
            localDict[token] = +1
    
    return localDict

def preProcess(text):
    # Should return a list of tokens
    lemmatizer = WordNetLemmatizer()
    filtered_tokens=[]
    lemmatized_tokens = []
    stop_words = set(stopwords.words('english'))
    text = text.translate(table)
    for w in text.split(" "):
        if w not in stop_words:
            lemmatized_tokens.append(lemmatizer.lemmatize(w.lower()))
        filtered_tokens = [' '.join(l) for l in nltk.bigrams(lemmatized_tokens)] + lemmatized_tokens
    return filtered_tokens


# ss = cls.classify_many(map(lambda t: t[0], xfTestData))


app = Flask(__name__)
@app.route('/')
@app.route('/first')
def first():
    return render_template('first.html')
    
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/index')
def index():
 	return render_template("index.html")
 
@app.route('/predict')
def predict():
    text = request.args.get('news')
    input_data = text.rstrip()
    rating = request.args.get('rating')
    verified = request.args.get('verified_options')
    category = request.args.get('category_options')
    rating = str(rating)

	# tfidf_test = tfidf_vectorizer.transform(input_data)
	# #predicting the input
	# y_pred = pac.predict(tfidf_test)
    # #output=y_pred[0]
	# if y_pred[0] == 0:
	#     xtr = "Real"
	# else:
	#     xtr = "Fake"
	# return render_template('index.html', prediction_text='Review is {}'.format(xtr)) 

    xfTestData = []
    xfTestData.append((toFeatureVector(rating, verified, category, preProcess(input_data)),rating))

    ss = cls.classify_many(map(lambda t: t[0], xfTestData))
    if ss[0] == 1:
        xtr = "Real"
    else:
        xtr = "Fake"
    return render_template('index.html', prediction_text='Review is {}'.format(xtr))
    print("abcdef")

if __name__=='__main__':
    app.run(debug=True)
