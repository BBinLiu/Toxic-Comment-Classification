import pandas as pd
from pickle import dump
from pickle import load
import numpy as np
import Preprocess
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def read():
    # import tain and test data
    data = pd.read_csv('data/train.csv')[:20000]
    train = data[:16000]
    test = data[16000:]
    # fill the null for test and training data
    train = train.fillna(' ')
    test = test.fillna(' ')
    return train, test

def train(train, test):
    # create the training variable
    X, x_test, vect_word = Preprocess.vectorizer(train, test)
    # create the target variable
    target_col = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    y = train[target_col]
    y_test = test[target_col]
    prd = np.zeros((x_test.shape[0], y_test.shape[1]))
    # use logistic regression to train data on each category
    for i, col in enumerate(target_col):
        lr = LogisticRegression(C=2, random_state=i, class_weight='balanced')
        lr.fit(X, y[col])
        # save models in different pikle files
        output = open('models/' + col + '.pkl', 'wb')
        print('Saving model in ' + col + '.pkl')
        dump(lr, output, -1)
        output.close()
        # predict on the test data
        prd[:, i] = lr.predict_proba(x_test)[:, 1]
    # calculate the accuracy score for each category
    accuracy = {}
    for col in target_col:
        print(col + ' Accuracy Score:')
        pred = lr.predict(x_test)
        score = accuracy_score(y_test[col], pred)
        accuracy[col] = score
        print(accuracy_score(y_test[col], pred))
    return accuracy, vect_word

def predict(vect_word, comment):
    # use the model created to predict on new sentences input
    target_col = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    scores = {}
    for col in target_col:
        input = open('models/' + col + '.pkl', 'rb')
        model = load(input)
        to_predict = [comment]
        t = vect_word.transform(to_predict)
        score = model.predict(t)
        scores[col] = score
        print(col + ' score is: ' + str(score))
        input.close()
    return scores