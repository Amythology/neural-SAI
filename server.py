import os
from flask import Flask, request, jsonify
from flask_cors import CORS 
from transformers import pipeline

app = Flask(__name__)
CORS(app)

print("Initializing Deep Emotion pipeline...")
# Using DistilRoBERTa fine-tuned for 7 distinct emotions
emotion_model = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", top_k=None)
print("Circumplex Engine Online.")

# Structural mapping of emotions onto the Valence (V) and Arousal (A) plane [-1.0 to 1.0]
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
        # Get probability distributions for all 7 emotions
        results = emotion_model(text)[0]
        
        weighted_v = 0.0
        weighted_a = 0.0
        
        top_emotion = results[0]['label']
        top_score = results[0]['score']

        # Calculate coordinates using weighted averages of all detected emotions
        for res in results:
            label = res['label']
            score = res['score']
            v, a = EMOTION_COORDS[label]
            weighted_v += v * score
            weighted_a += a * score

        return jsonify({
            "text": text,
            "primary_emotion": top_emotion.capitalize(),
            "valence": round(weighted_v, 3),   # X-axis
            "arousal": round(weighted_a, 3),   # Y-axis
            "confidence": f"{round(top_score * 100, 2)}%"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)