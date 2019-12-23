import nltk
from nltk.stem import WordNetLemmatizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def tokenizer(comments):
    new_comments = []
    for comment in comments:
        new_comments.append([w.lower() for w in nltk.word_tokenize(comment)])
    return new_comments

def remove_stopwords_punctuation(comments):
    stopwords = nltk.corpus.stopwords.words('english')
    new_comments = []
    for comment in comments:
        clean_tokens = [token for token in comment if token not in stopwords
                        and any(c.isalpha() for c in token)]
        new_comments.append(clean_tokens)
    return new_comments

def lemmatizer(comments):
    wordnet_lemmatizer = WordNetLemmatizer()
    new_comments = []
    for comment in comments:
        clean_tokens = [wordnet_lemmatizer.lemmatize(word) for word in comment]
        new_comments.append(clean_tokens)
    return new_comments

def join_token(comments):
    new_comments = []
    for comment in comments:
        text = ' '.join([w for w in comment])
        new_comments.append(text)
    return new_comments

def vectorizer(train, test):
    # create the tfidf vectorizer that utilized ngrams
    vect_word = TfidfVectorizer(max_features=8000, lowercase=True, analyzer='word',
                                stop_words='english', ngram_range=(1, 3), dtype=np.float32)
    # use the tfidf vectorizer to tranform the training data
    X = vect_word.fit_transform(train['comment_text'])
    x_test = vect_word.transform(test['comment_text'])
    return X, x_test, vect_word
