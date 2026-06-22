import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for all domains, or specify your frontend URL
CORS(app)

print("Initializing Lightweight API Relay Server...")

# 1. HUGGING FACE API SETUP
# We use the exact same model, but hosted on Hugging Face's servers.
API_URL = "https://api-inference.huggingface.co/models/bhadresh-savani/distilbert-base-uncased-emotion"

# Grab the token from Render Environment Variables
# If you don't have a token, you can run this without one for testing, 
# but HF will rate-limit you heavily.
HF_TOKEN = os.environ.get('HF_TOKEN')
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

# Map DistilBERT emotion labels to Valence/Arousal coordinates [-1.0 to 1.0]
EMOTION_COORDS = {
    'joy': (0.8, 0.4),
    'love': (0.8, -0.2),      
    'surprise': (0.4, 0.9),   
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
        # Forward the text to Hugging Face
        response = requests.post(API_URL, headers=headers, json={"inputs": text})
        api_data = response.json()

        # Handle the case where the free HF API is "waking up"
        if isinstance(api_data, dict) and 'error' in api_data:
            wait_time = int(api_data.get('estimated_time', 15))
            return jsonify({"error": f"The AI engine is waking up from sleep. Please try again in {wait_time} seconds."}), 503

        # HF returns a list of lists, we just need the first item
        results = api_data[0]
        
        weighted_v = 0.0
        weighted_a = 0.0
        
        top_emotion = results[0]['label']
        top_score = results[0]['score']

        # Calculate coordinates
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

    except requests.exceptions.RequestException as e:
        print(f"Network error to HF: {e}")
        return jsonify({"error": "Failed to connect to the external AI provider."}), 502
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)