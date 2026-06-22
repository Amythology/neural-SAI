import os
import gc
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS 
from transformers import pipeline

# 1. ENFORCE STRICT MEMORY CONSTRAINTS
torch.set_num_threads(1)
if hasattr(torch, 'set_num_interop_threads'):
    torch.set_num_interop_threads(1)

app = Flask(__name__)
CORS(app)

print("Loading ultra-lightweight DistilBERT Emotion engine...")

# 2. LOAD COMPACT 255MB TRANSFORMER 
emotion_model = pipeline(
    "text-classification", 
    model="bhadresh-savani/distilbert-base-uncased-emotion", 
    top_k=None,
    low_cpu_mem_usage=True
)

# 3. IMMEDIATE PURGE OF SYSTEM CACHE
gc.collect()
print("Circumplex Engine Online. RAM footprint minimized.")

# Map DistilBERT emotion labels to Valence/Arousal coordinates [-1.0 to 1.0]
EMOTION_COORDS = {
    'joy': (0.8, 0.4),
    'love': (0.8, -0.2),      # Pleasant, low-intensity/calm energy
    'surprise': (0.4, 0.9),   # High energy, slightly positive valence
    'anger': (-0.7, 0.8),
    'fear': (-0.6, 0.8),
    'sadness': (-0.8, -0.6)
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

        # Calculate coordinates using weights from the lighter DistilBERT array
        for res in results:
            label = res['label'].lower()
            score = res['score']
            
            if label in EMOTION_COORDS:
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