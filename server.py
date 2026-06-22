import os
import gc
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS 
from transformers import pipeline

# 1. CRITICAL RENDER RAM FIX: Force single-threaded execution before loading anything
torch.set_num_threads(1)

app = Flask(__name__)
CORS(app)

print("Initializing Deep Emotion pipeline with strict memory controls...")

# 2. OPTIMIZED MODEL LOADING: Prevent RAM duplication
emotion_model = pipeline(
    "text-classification", 
    model="j-hartmann/emotion-english-distilroberta-base", 
    top_k=None,
    low_cpu_mem_usage=True  # Slashes startup RAM spike in half
)

# 3. GARBAGE COLLECTION: Clean up RAM cache instantly
gc.collect()

print("Circumplex Engine Online within memory safety limits.")

EMOTION_COORDS = {
    'joy': (0.8, 0.4),
    'anger': (-0.7, 0.8),
    'fear': (-0.6, 0.8),
    'sadness': (-0.8, -0.6),
    'surprise': (0.4, 0.9),
    'disgust': (-0.8, 0.4),
    'neutral': (0.0, 0.0)
}

@app.route('/analyze', methods=['POST'])
def analyze():
    req = request.get_json()
    text = req.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        results = emotion_model(text)[0]
        
        weighted_v = 0.0
        weighted_a = 0.0
        
        top_emotion = results[0]['label']
        top_score = results[0]['score']

        for res in results:
            label = res['label']
            score = res['score']
            v, a = EMOTION_COORDS[label]
            weighted_v += v * score
            weighted_a += a * score

        return jsonify({
            "text": text,
            "primary_emotion": top_emotion.capitalize(),
            "valence": round(weighted_v, 3),
            "arousal": round(weighted_a, 3),
            "confidence": f"{round(top_score * 100, 2)}%"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)