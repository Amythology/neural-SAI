# Save this strictly as: math_playground.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

class CustomLogisticRegression:
    def __init__(self, learning_rate=0.1, n_iterations=1000):
        self.lr = learning_rate
        self.n_iters = n_iterations
        self.weights = None
        self.bias = None

    def _sigmoid(self, z):
        z = np.clip(z, -250, 250)
        return 1 / (1 + np.exp(-z))

    def fit(self, X, y):
        if hasattr(X, "toarray"): X = X.toarray()
        y = np.array(y) 
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        for _ in range(self.n_iters):
            linear_model = np.dot(X, self.weights) + self.bias
            y_predicted = self._sigmoid(linear_model)
            dw = (1 / n_samples) * np.dot(X.T, (y_predicted - y))
            db = (1 / n_samples) * np.sum(y_predicted - y)
            self.weights -= self.lr * dw
            self.bias -= self.lr * db

    def predict_proba(self, X):
        if hasattr(X, "toarray"): X = X.toarray()
        linear_model = np.dot(X, self.weights) + self.bias
        return self._sigmoid(linear_model)

    def predict(self, X, threshold=0.5):
        return [1 if p >= threshold else 0 for p in self.predict_proba(X)]

# Small dataset for local testing
corpus = ["I love this!", "Best thing ever.", "This is terrible.", "I hate it so much."]
labels = [1, 1, 0, 0]

vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
X_train_tfidf = vectorizer.fit_transform(corpus)

custom_model = CustomLogisticRegression(learning_rate=0.5, n_iterations=2000)
custom_model.fit(X_train_tfidf, labels)

print("\n🤖 Custom Math Analyzer Ready! Type 'quit' to exit.")
while True:
    user_text = input("Enter text: ")
    if user_text.lower() == 'quit': break
    if not user_text.strip(): continue

    vec_text = vectorizer.transform([user_text])
    pred_class = custom_model.predict(vec_text)[0]
    print("--> Positive" if pred_class == 1 else "--> Negative")