import re
import numpy as np
from flask import Flask, request, jsonify
import gensim.downloader as api
import joblib
from flask_cors import CORS 


# 1. Server initialization and memory loading
app = Flask(__name__)
CORS(app)
glove = api.load('glove-twitter-25')
clf = joblib.load('model.joblib')

def vectorize(text):
    clean = re.sub(r'[^\w\s]', '', text.lower()).split()
    vecs = [glove[w] for w in clean if w in glove]
    return np.mean(vecs, axis=0) if vecs else np.zeros(25)

# 2. Route handling and inference logic
@app.route('/analyze', methods=['POST'])
def analyze():
    req = request.get_json()
    text = req.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    vec = vectorize(text).reshape(1, -1)
    pred = clf.predict(vec)[0]
    prob = clf.predict_proba(vec)[0]

    return jsonify({
        "text": text,
        "sentiment": "Positive" if pred == 1 else "Negative",
        "confidence": f"{round(max(prob) * 100, 2)}%"
    })

import os
# ...
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)