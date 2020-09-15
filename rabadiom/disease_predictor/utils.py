import pandas as pd
from itertools import groupby

from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB, ComplementNB
from sklearn.linear_model.logistic import LogisticRegression

import pickle


df = pd.read_csv("C:/Users/jaski/OneDrive/Desktop/diseases.csv")

symptoms = list(df["symptom"].unique())
unique_symptoms = []
uniq = []
for s in symptoms:
    uniq.append((s,s))
uniq.sort()
unique_symptoms.append(('Select', None))
for s in uniq:
  unique_symptoms.append(s)

def predict_disease(symptoms):
    predictions = []
    for symptom in symptoms:
        prediction = {}
        disease = df["disease"].where(df["symptom"]==symptom)
        tfidf = df["tfidf"].where(df["symptom"]==symptom)
        disease = list(disease.dropna())
        tfidf = list(tfidf.dropna())
        for dis,tf in zip(disease,tfidf):
            prediction.update({dis:tf})
        predictions.append([symptom,prediction])
    for prediction in predictions:
        for pred in predictions:
            if pred[0] == prediction[0]:
                #print("skipped")
                pass
            else:
                for disease, tfidf in pred[1].items():
                    if disease in prediction[1]:
                        prediction[1][disease] += tfidf
    s = []
    final_pred = []
    pred = []
    for prediction in predictions:
        s.append(sorted(prediction[1].items(), key=lambda kv: kv[1], reverse=True))
    for ss in s:
        for sss in ss[:4]:
            pred.append(sss)
    #final_pred = set(final_pred)
    pred.sort()
    for _, group in groupby(pred, lambda x: x[0]):
        final_pred.append(max(group))
    final_pred = sorted(final_pred, key=lambda x: x[1], reverse=True)
    return list(final_pred)


def generate_test_data(sym):
    data = []
    for s in symptoms:
        t = 0
        if s in sym:
            t = 1
        data.append(t)
    return data

def num_to_disease(data, df):
    data = data[0]
    return df["diseases"].iloc[data]


def predict_using_ml(sym):
    df = pd.read_csv("C:/Users/jaski/OneDrive/Desktop/dis_to_sym.csv")
    data = [generate_test_data(sym)]
    logistic_regression_pkl = open("C:/Users/jaski/OneDrive/Desktop/major project/Flask-App/rabadiom/disease_predictor/logistic_regression_pkl","rb")
    bernoulli_pkl = open("C:/Users/jaski/OneDrive/Desktop/major project/Flask-App/rabadiom/disease_predictor/bernoulli_pkl","rb")
    complement_pkl = open("C:/Users/jaski/OneDrive/Desktop/major project/Flask-App/rabadiom/disease_predictor/complement_pkl","rb")
    tree_regressor_pkl = open("C:/Users/jaski/OneDrive/Desktop/major project/Flask-App/rabadiom/disease_predictor/tree_regressor_pkl","rb")
    tree_classifier_pkl = open("C:/Users/jaski/OneDrive/Desktop/major project/Flask-App/rabadiom/disease_predictor/tree_classifier_pkl","rb")

    logistic_regression = pickle.load(logistic_regression_pkl)
    bernoulli = pickle.load(bernoulli_pkl)
    complement = pickle.load(complement_pkl)
    tree_regressor = pickle.load(tree_regressor_pkl)
    tree_classifier = pickle.load(tree_classifier_pkl)

    final_pred = []
    final_pred.append([num_to_disease(logistic_regression.predict(data), df), "Logistic Regression"])
    final_pred.append([num_to_disease(bernoulli.predict(data), df), "Bernoulli Naive Bayes"])
    final_pred.append([num_to_disease(complement.predict(data), df), "Complement Naive Bayes"])
    final_pred.append([num_to_disease(tree_classifier.predict(data), df), "Decision Tree Classifier"])
    #final_pred.append([tree_regressor.predict(data), "Decision Tree Regressor"])
    #final_pred = sorted(final_pred, key=lambda x: x[1], reverse=True)

    return list(final_pred)
