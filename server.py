import os
import re
import math
import nltk
from flask import Flask, request, jsonify
from flask_cors import CORS
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from emotion_lexicon_data import EMOTION_LEXICON

# 1. DOWNLOAD VADER LEXICON (Runs once, takes < 1 second)
nltk.download('vader_lexicon', quiet=True)

app = Flask(__name__)
CORS(app)

print("Initializing Smart Heuristic Engine (No ML Bloat)...")
sia = SentimentIntensityAnalyzer()
print(f"Loaded emotion lexicon: {len(EMOTION_LEXICON)} words")

# --- THE LOGIC ---
#
# Architecture: VADER gives us Valence (pleasant/unpleasant) for free, since
# it's a well-tuned rule-based lexicon. The piece VADER doesn't give us is
# Arousal (energy level), which is what actually separates emotions that
# share the same valence sign — e.g. Anger and Sadness are both "negative",
# but Anger is high-energy and Sadness is low-energy. EMOTION_LEXICON below
# is a word -> (emotion, arousal) map used to estimate that missing axis.
#
# EMOTION_LEXICON was built by hand-seeding ~70 core emotion words per
# category, then expanding each seed into its WordNet synonyms/similar-tos
# OFFLINE (see build_lexicon.py) to get ~900 words of coverage. We do NOT
# import nltk.corpus.wordnet here at runtime: loading WordNet's corpus index
# costs ~180MB of RAM on first access, which is too much headroom to give up
# on a 512MB instance. Baking the expanded result into a static dict gives
# us the coverage benefit at zero runtime cost.

# 2D Emotion Map (Valence, Arousal) — coordinates per Russell's Circumplex Model.
EMOTION_CENTROIDS = {
    "Anger":       {"v": -0.7, "a": 0.7},
    "Fear":        {"v": -0.6, "a": 0.6},
    "Sadness":     {"v": -0.7, "a": -0.5},
    "Disgust":     {"v": -0.7, "a": 0.1},
    "Joy":         {"v": 0.75, "a": 0.6},
    "Contentment": {"v": 0.6, "a": -0.5},
    "Neutral":     {"v": 0.0, "a": 0.0},
}

WORD_RE = re.compile(r"[a-z']+")


def tokenize(text):
    """Lowercase + strip punctuation so 'amazing!' / 'unacceptable,' match the lexicon."""
    return WORD_RE.findall(text.lower())


def lexicon_arousal_and_votes(words):
    """
    Scan tokens against EMOTION_LEXICON.
    Returns (average_arousal_or_None, votes) where votes counts how many
    matched words point at each emotion. votes lets us break ties in
    get_closest_emotion when two emotions' centroids are geometrically close
    (e.g. Anger/Disgust/Fear all live in negative-valence space).
    """
    arousal_hits = []
    votes = {}
    for w in words:
        if w in EMOTION_LEXICON:
            emotion, arousal = EMOTION_LEXICON[w]
            arousal_hits.append(arousal)
            votes[emotion] = votes.get(emotion, 0) + 1
    if arousal_hits:
        return sum(arousal_hits) / len(arousal_hits), votes
    return None, votes


def calculate_arousal(words, vader_scores, compound, votes):
    """
    Primary path: average arousal of any matched lexicon words, blended
    slightly with overall VADER sentiment intensity so a single matched word
    doesn't fully override a much stronger overall sentiment signal.

    Fallback path (no lexicon words matched): scale arousal with how much
    sentiment VADER actually found (pos + neg share), not a fixed offset.
    This is the fix for the original bug where neutral text with no
    sentiment (pos=0, neg=0) was forced to arousal = -1.0 ("very calm"),
    which wrongly classified plain neutral sentences as Contentment.
    """
    lexicon_arousal, _ = lexicon_arousal_and_votes(words)

    if lexicon_arousal is not None:
        intensity_signal = vader_scores['pos'] + vader_scores['neg']
        direction = 1 if lexicon_arousal >= 0 else -1
        return (lexicon_arousal * 0.75) + (intensity_signal * direction * 0.25)

    intensity = vader_scores['pos'] + vader_scores['neg']  # 0 (neutral) .. ~1 (strong)
    direction = 1 if compound >= 0 else -1
    return direction * intensity * 0.5


def get_emotion_distances(v, a, votes):
    """
    Euclidean distance from (v, a) to EVERY centroid, with a small discount
    applied to whichever emotion the matched lexicon words voted for most.
    This lets explicit word choice win ties in regions where centroids
    overlap (e.g. Anger and Disgust are both negative/mid-high arousal).
    Returns distances for all 7 emotions (not just the winner) so callers
    can build a full ranked breakdown instead of a single label.
    """
    distances = {}
    for emotion, coords in EMOTION_CENTROIDS.items():
        distances[emotion] = math.sqrt((v - coords["v"]) ** 2 + (a - coords["a"]) ** 2)

    if votes:
        top_voted = max(votes, key=votes.get)
        distances[top_voted] *= 0.6

    return distances


def distances_to_scores(distances):
    """
    Convert raw distances into a 0-100 ranked breakdown across all emotions.
    max_dist is the diagonal of the (v, a) plane in [-1,1] x [-1,1] — the
    largest distance two points in this space can be apart — so distance 0
    maps to 100% similarity and distance max_dist maps to 0%. Scores are
    then renormalized to sum to 100, so the result reads like a breakdown
    ("Anger 58%, Disgust 19%, Fear 12%, ...") instead of 7 numbers that
    don't relate to each other.
    """
    max_dist = math.sqrt(8)
    similarities = {e: max(0.0, 1 - (d / max_dist)) for e, d in distances.items()}
    total = sum(similarities.values())

    if total == 0:
        equal_share = round(100 / len(similarities), 2)
        return {e: equal_share for e in similarities}

    return {e: round((s / total) * 100, 2) for e, s in similarities.items()}


# --- THE API ROUTE ---

@app.route('/analyze', methods=['POST'])
def analyze():
    req = request.get_json()
    text = req.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # 1. Get Valence directly from VADER
        scores = sia.polarity_scores(text)
        valence = scores['compound']

        # 2. Tokenize once, reuse for arousal + voting
        words = tokenize(text)
        _, votes = lexicon_arousal_and_votes(words)

        # 3. Calculate Arousal using lexicon hits (or sentiment-scaled fallback)
        arousal = calculate_arousal(words, scores, valence, votes)
        arousal = max(-1.0, min(1.0, arousal))

        # 4. Distance to every centroid, then pick the nearest as the label
        distances = get_emotion_distances(valence, arousal, votes)
        top_emotion = min(distances, key=distances.get)

        # 5. True-neutral override: only when VADER finds essentially no
        #    sentiment AND no emotion words matched. Without this, "I went to
        #    the store" and similar flat statements would still get pulled
        #    toward whichever centroid is nearest the origin by chance.
        if scores['neu'] > 0.95 and not votes:
            top_emotion = "Neutral"
            valence, arousal = 0.0, 0.0
            distances = get_emotion_distances(valence, arousal, {})

        # 6. Confidence proxy based on how strong the coordinates are
        if top_emotion == "Neutral":
            confidence = f"{round(scores['neu'] * 100, 2)}%"
        else:
            confidence = f"{round(((abs(valence) + abs(arousal)) / 2) * 100, 2)}%"

        # 7. Full ranked breakdown across all 7 emotions, not just the winner.
        #    Sorted descending so emotions[0] always matches primary_emotion.
        emotion_scores = distances_to_scores(distances)
        emotions = [
            {"emotion": emotion, "score": score}
            for emotion, score in sorted(emotion_scores.items(), key=lambda kv: -kv[1])
        ]

        return jsonify({
            "text": text,
            "primary_emotion": top_emotion,
            "valence": round(valence, 3),
            "arousal": round(arousal, 3),
            "confidence": confidence,
            "emotions": emotions
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)