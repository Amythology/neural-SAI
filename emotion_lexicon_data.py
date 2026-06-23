"""
EMOTION_LEXICON
---------------
Static word -> (emotion, arousal) map used by server.py to estimate the
Arousal axis that VADER doesn't give us (VADER only scores Valence).

Design notes:
- Hand-curated, ~280 words across the 6 non-neutral categories used in
  EMOTION_CENTROIDS (Anger, Fear, Sadness, Disgust, Joy, Contentment).
- No WordNet / nltk.corpus import at runtime — this is a flat dict baked
  ahead of time, so the only memory cost at runtime is the dict itself
  (a few hundred KB at most). This keeps the app inside Render's free
  512MB tier alongside VADER.
- Arousal values are signed floats roughly in [-0.9, 0.9], scaled to sit
  near (but with spread around) that emotion's centroid arousal in
  EMOTION_CENTROIDS:
    Anger        a=+0.7   -> words range ~0.4 to 0.95 (mild to extreme)
    Fear         a=+0.6   -> words range ~0.4 to 0.9
    Joy          a=+0.6   -> words range ~0.4 to 0.9
    Disgust      a=+0.1   -> words range ~0.0 to 0.3 (low/flat energy)
    Sadness      a=-0.5   -> words range ~-0.3 to -0.6 (low energy)
    Contentment  a=-0.5   -> words range ~-0.3 to -0.6 (low energy)
  The spread within a category lets mild words (e.g. "annoyed") and
  intense words (e.g. "furious") land at different points instead of
  collapsing every hit in a category to one identical value.
- Only single lowercase alphabetic tokens are used as keys, since
  tokenize() in server.py strips punctuation/spacing before lookup
  (no multi-word phrases like "fed up").
"""

EMOTION_LEXICON = {

    # ---------------- ANGER (high arousal, negative) ----------------
    "angry": ("Anger", 0.65), "mad": ("Anger", 0.55), "furious": ("Anger", 0.9),
    "enraged": ("Anger", 0.95), "rage": ("Anger", 0.95), "raging": ("Anger", 0.85),
    "irate": ("Anger", 0.85), "livid": ("Anger", 0.9), "outraged": ("Anger", 0.85),
    "outrage": ("Anger", 0.8), "infuriated": ("Anger", 0.9), "infuriating": ("Anger", 0.85),
    "fuming": ("Anger", 0.8), "seething": ("Anger", 0.8), "wrathful": ("Anger", 0.85),
    "indignant": ("Anger", 0.6), "resentful": ("Anger", 0.5), "resentment": ("Anger", 0.5),
    "hostile": ("Anger", 0.65), "hostility": ("Anger", 0.65), "aggravated": ("Anger", 0.6),
    "annoyed": ("Anger", 0.4), "annoying": ("Anger", 0.4), "irritated": ("Anger", 0.5),
    "irritating": ("Anger", 0.5), "frustrated": ("Anger", 0.55), "frustrating": ("Anger", 0.55),
    "agitated": ("Anger", 0.6), "bitter": ("Anger", 0.45), "vengeful": ("Anger", 0.7),
    "hateful": ("Anger", 0.7), "hate": ("Anger", 0.65), "hatred": ("Anger", 0.7),
    "cross": ("Anger", 0.4), "exasperated": ("Anger", 0.6), "incensed": ("Anger", 0.85),
    "riled": ("Anger", 0.6), "provoked": ("Anger", 0.55), "offended": ("Anger", 0.45),
    "insulted": ("Anger", 0.5), "betrayed": ("Anger", 0.6), "vindictive": ("Anger", 0.65),
    "spiteful": ("Anger", 0.6), "snapped": ("Anger", 0.6), "yelling": ("Anger", 0.7),
    "screaming": ("Anger", 0.75), "shouting": ("Anger", 0.65), "grudge": ("Anger", 0.4),
    "temper": ("Anger", 0.55), "tantrum": ("Anger", 0.65), "loathing": ("Anger", 0.55),
    "contempt": ("Anger", 0.5), "scorn": ("Anger", 0.5), "disdain": ("Anger", 0.45),
    "outburst": ("Anger", 0.65), "confrontational": ("Anger", 0.6), "combative": ("Anger", 0.65),
    "belligerent": ("Anger", 0.65), "aggressive": ("Anger", 0.6), "volatile": ("Anger", 0.6),
    "explosive": ("Anger", 0.7), "boiling": ("Anger", 0.65), "simmering": ("Anger", 0.45),
    "pissed": ("Anger", 0.65), "ticked": ("Anger", 0.45), "fed": ("Anger", 0.4),

    # ---------------- FEAR (high arousal, negative) ----------------
    "afraid": ("Fear", 0.6), "scared": ("Fear", 0.65), "terrified": ("Fear", 0.9),
    "horrified": ("Fear", 0.85), "petrified": ("Fear", 0.85), "frightened": ("Fear", 0.65),
    "fearful": ("Fear", 0.6), "anxious": ("Fear", 0.55), "anxiety": ("Fear", 0.55),
    "nervous": ("Fear", 0.5), "worried": ("Fear", 0.5), "worry": ("Fear", 0.45),
    "panicked": ("Fear", 0.85), "panicking": ("Fear", 0.85), "panic": ("Fear", 0.85),
    "dread": ("Fear", 0.65), "dreadful": ("Fear", 0.55), "alarmed": ("Fear", 0.65),
    "alarming": ("Fear", 0.6), "apprehensive": ("Fear", 0.5), "uneasy": ("Fear", 0.45),
    "terror": ("Fear", 0.9), "horror": ("Fear", 0.85), "spooked": ("Fear", 0.55),
    "jumpy": ("Fear", 0.5), "jittery": ("Fear", 0.5), "trembling": ("Fear", 0.6),
    "shaking": ("Fear", 0.55), "paranoid": ("Fear", 0.6), "threatened": ("Fear", 0.55),
    "vulnerable": ("Fear", 0.4), "insecure": ("Fear", 0.4), "intimidated": ("Fear", 0.55),
    "startled": ("Fear", 0.6), "shocked": ("Fear", 0.6), "stunned": ("Fear", 0.5),
    "distressed": ("Fear", 0.55), "suspicious": ("Fear", 0.4), "wary": ("Fear", 0.4),
    "timid": ("Fear", 0.35), "cowering": ("Fear", 0.6), "fright": ("Fear", 0.65),
    "spooky": ("Fear", 0.5), "haunted": ("Fear", 0.55), "ominous": ("Fear", 0.5),
    "foreboding": ("Fear", 0.55), "tense": ("Fear", 0.5), "restless": ("Fear", 0.45),
    "unsettled": ("Fear", 0.45), "scary": ("Fear", 0.55), "terrifying": ("Fear", 0.85),
    "menacing": ("Fear", 0.55), "creepy": ("Fear", 0.45), "freaked": ("Fear", 0.65),
    "overwhelmed": ("Fear", 0.55),

    # ---------------- SADNESS (low arousal, negative) ----------------
    "sad": ("Sadness", -0.35), "unhappy": ("Sadness", -0.35), "depressed": ("Sadness", -0.5),
    "depressing": ("Sadness", -0.45), "miserable": ("Sadness", -0.45), "sorrowful": ("Sadness", -0.5),
    "grief": ("Sadness", -0.45), "grieving": ("Sadness", -0.45), "heartbroken": ("Sadness", -0.4),
    "devastated": ("Sadness", -0.4), "gloomy": ("Sadness", -0.5), "melancholy": ("Sadness", -0.55),
    "despair": ("Sadness", -0.45), "despondent": ("Sadness", -0.55), "dejected": ("Sadness", -0.5),
    "downcast": ("Sadness", -0.5), "mournful": ("Sadness", -0.55), "somber": ("Sadness", -0.6),
    "blue": ("Sadness", -0.35), "lonely": ("Sadness", -0.4), "loneliness": ("Sadness", -0.4),
    "hopeless": ("Sadness", -0.45), "forlorn": ("Sadness", -0.55), "woeful": ("Sadness", -0.5),
    "tearful": ("Sadness", -0.35), "crying": ("Sadness", -0.3), "weeping": ("Sadness", -0.35),
    "sobbing": ("Sadness", -0.35), "heartache": ("Sadness", -0.4), "disheartened": ("Sadness", -0.5),
    "dismal": ("Sadness", -0.55), "bleak": ("Sadness", -0.55), "dispirited": ("Sadness", -0.5),
    "downhearted": ("Sadness", -0.5), "regretful": ("Sadness", -0.35), "remorseful": ("Sadness", -0.35),
    "ashamed": ("Sadness", -0.3), "empty": ("Sadness", -0.45), "numb": ("Sadness", -0.5),
    "drained": ("Sadness", -0.5), "exhausted": ("Sadness", -0.45), "weary": ("Sadness", -0.5),
    "fatigued": ("Sadness", -0.5), "lethargic": ("Sadness", -0.6), "listless": ("Sadness", -0.6),
    "sluggish": ("Sadness", -0.55), "gloom": ("Sadness", -0.5), "sorrow": ("Sadness", -0.45),
    "anguish": ("Sadness", -0.35), "abandoned": ("Sadness", -0.4), "rejected": ("Sadness", -0.4),
    "isolated": ("Sadness", -0.45), "neglected": ("Sadness", -0.45), "longing": ("Sadness", -0.3),
    "nostalgic": ("Sadness", -0.25), "wistful": ("Sadness", -0.3), "defeated": ("Sadness", -0.45),
    "discouraged": ("Sadness", -0.45), "disappointed": ("Sadness", -0.4), "disappointing": ("Sadness", -0.4),
    "crushed": ("Sadness", -0.4), "broken": ("Sadness", -0.4), "hurting": ("Sadness", -0.35),

    # ---------------- DISGUST (low/flat arousal, negative) ----------------
    "disgusted": ("Disgust", 0.2), "disgusting": ("Disgust", 0.25), "disgust": ("Disgust", 0.2),
    "gross": ("Disgust", 0.15), "revolting": ("Disgust", 0.3), "repulsed": ("Disgust", 0.3),
    "repulsive": ("Disgust", 0.3), "nauseated": ("Disgust", 0.25), "nauseating": ("Disgust", 0.25),
    "sickened": ("Disgust", 0.25), "sickening": ("Disgust", 0.25), "vile": ("Disgust", 0.2),
    "foul": ("Disgust", 0.15), "putrid": ("Disgust", 0.2), "repugnant": ("Disgust", 0.25),
    "distasteful": ("Disgust", 0.1), "yucky": ("Disgust", 0.1), "icky": ("Disgust", 0.1),
    "gag": ("Disgust", 0.3), "gagging": ("Disgust", 0.3), "queasy": ("Disgust", 0.15),
    "revulsion": ("Disgust", 0.3), "loathsome": ("Disgust", 0.25), "abhorrent": ("Disgust", 0.3),
    "offensive": ("Disgust", 0.15), "filthy": ("Disgust", 0.1), "grimy": ("Disgust", 0.05),
    "squeamish": ("Disgust", 0.1), "appalled": ("Disgust", 0.3), "appalling": ("Disgust", 0.3),
    "cringe": ("Disgust", 0.15), "cringing": ("Disgust", 0.15), "cringeworthy": ("Disgust", 0.15),
    "contaminated": ("Disgust", 0.05), "rotten": ("Disgust", 0.1), "rancid": ("Disgust", 0.15),
    "stale": ("Disgust", 0.0), "unsanitary": ("Disgust", 0.05), "repellent": ("Disgust", 0.15),
    "vomit": ("Disgust", 0.3), "vomiting": ("Disgust", 0.3), "retch": ("Disgust", 0.3),
    "retching": ("Disgust", 0.3), "ew": ("Disgust", 0.1), "eww": ("Disgust", 0.1),
    "yuck": ("Disgust", 0.1), "nasty": ("Disgust", 0.15),

    # ---------------- JOY (high arousal, positive) ----------------
    "happy": ("Joy", 0.5), "joyful": ("Joy", 0.7), "joyous": ("Joy", 0.7),
    "ecstatic": ("Joy", 0.9), "elated": ("Joy", 0.8), "thrilled": ("Joy", 0.85),
    "excited": ("Joy", 0.8), "exciting": ("Joy", 0.7), "ecstasy": ("Joy", 0.9),
    "delighted": ("Joy", 0.6), "ebullient": ("Joy", 0.75), "exhilarated": ("Joy", 0.85),
    "exhilarating": ("Joy", 0.8), "cheerful": ("Joy", 0.5), "jubilant": ("Joy", 0.8),
    "euphoric": ("Joy", 0.85), "gleeful": ("Joy", 0.65), "exuberant": ("Joy", 0.8),
    "enthusiastic": ("Joy", 0.7), "elation": ("Joy", 0.8), "joy": ("Joy", 0.6),
    "bliss": ("Joy", 0.55), "blissful": ("Joy", 0.55), "overjoyed": ("Joy", 0.85),
    "giddy": ("Joy", 0.7), "thrilling": ("Joy", 0.75), "laughing": ("Joy", 0.55),
    "laughter": ("Joy", 0.55), "giggling": ("Joy", 0.5), "celebrating": ("Joy", 0.65),
    "celebration": ("Joy", 0.6), "triumphant": ("Joy", 0.7), "victorious": ("Joy", 0.7),
    "pumped": ("Joy", 0.75), "stoked": ("Joy", 0.75), "hyped": ("Joy", 0.8),
    "amazing": ("Joy", 0.5), "wonderful": ("Joy", 0.45), "fantastic": ("Joy", 0.5),
    "awesome": ("Joy", 0.5), "smiling": ("Joy", 0.4), "grinning": ("Joy", 0.45),
    "bubbly": ("Joy", 0.55), "lively": ("Joy", 0.5), "energized": ("Joy", 0.6),
    "vibrant": ("Joy", 0.5), "radiant": ("Joy", 0.45), "delightful": ("Joy", 0.45),
    "playful": ("Joy", 0.45), "festive": ("Joy", 0.5), "yay": ("Joy", 0.6),
    "woohoo": ("Joy", 0.7),

    # ---------------- CONTENTMENT (low arousal, positive) ----------------
    "content": ("Contentment", -0.35), "contented": ("Contentment", -0.4),
    "calm": ("Contentment", -0.5), "relaxed": ("Contentment", -0.55),
    "peaceful": ("Contentment", -0.55), "serene": ("Contentment", -0.6),
    "tranquil": ("Contentment", -0.6), "satisfied": ("Contentment", -0.4),
    "satisfying": ("Contentment", -0.35), "comfortable": ("Contentment", -0.45),
    "cozy": ("Contentment", -0.5), "soothed": ("Contentment", -0.5),
    "soothing": ("Contentment", -0.5), "restful": ("Contentment", -0.55),
    "mellow": ("Contentment", -0.5), "placid": ("Contentment", -0.6),
    "gentle": ("Contentment", -0.4), "easygoing": ("Contentment", -0.4),
    "settled": ("Contentment", -0.4), "secure": ("Contentment", -0.35),
    "grateful": ("Contentment", -0.3), "gratitude": ("Contentment", -0.3),
    "thankful": ("Contentment", -0.3), "blessed": ("Contentment", -0.3),
    "fulfilled": ("Contentment", -0.35), "harmonious": ("Contentment", -0.45),
    "balanced": ("Contentment", -0.4), "untroubled": ("Contentment", -0.5),
    "quiet": ("Contentment", -0.45), "still": ("Contentment", -0.5),
    "snug": ("Contentment", -0.5), "cherished": ("Contentment", -0.3),
    "appreciated": ("Contentment", -0.3), "loved": ("Contentment", -0.3),
    "nurtured": ("Contentment", -0.35), "pampered": ("Contentment", -0.35),
    "leisurely": ("Contentment", -0.45), "unhurried": ("Contentment", -0.45),
    "carefree": ("Contentment", -0.4), "lighthearted": ("Contentment", -0.35),
    "okay": ("Contentment", -0.3), "fine": ("Contentment", -0.3),
}