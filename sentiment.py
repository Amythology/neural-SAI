import re
import numpy as np
import gensim.downloader as api
from datasets import load_dataset
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# 1. Initialization and text vectorization mapping
glove = api.load('glove-twitter-25')

def vectorize(text):
    clean = re.sub(r'[^\w\s]', '', text.lower()).split()
    vecs = [glove[w] for w in clean if w in glove]
    return np.mean(vecs, axis=0) if vecs else np.zeros(25)

# 2. Dataset loading and preprocessing
print("Preparing data...")
data = load_dataset("stanfordnlp/imdb")
train = data['train'].shuffle(seed=42)
test = data['test'].shuffle(seed=42)

X_train = [vectorize(t) for t in train['text'][:5000]]
y_train = train['label'][:5000]
X_test = [vectorize(t) for t in test['text'][:1000]]
y_test = test['label'][:1000]

# 3. Model training and evaluation
print("Training model...")
clf = LogisticRegression(max_iter=1000)
clf.fit(X_train, y_train)

preds = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, preds) * 100:.2f}%")

# 4. Save artifacts
joblib.dump(clf, 'model.joblib')
print("Saved to model.joblib")