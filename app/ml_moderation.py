import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from joblib import dump, load
import nltk
from nltk.corpus import stopwords

# Download NLTK resources (do this once)
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

# Example: Data loading
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    return df['text'], df['label']

# Preprocessing function
def preprocess(text):
    # Lowercase, remove stopwords, simple cleaning
    words = [word for word in text.lower().split() if word.isalpha() and word not in STOPWORDS]
    return ' '.join(words)

# Model training pipeline
def train_model(X, y):
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(preprocessor=preprocess)),
        ('clf', LogisticRegression(max_iter=1000))
    ])
    pipeline.fit(X, y)
    return pipeline

# Model evaluation
def evaluate_model(model, X, y):
    preds = model.predict(X)
    print(classification_report(y, preds))

# Save/load model
def save_model(model, path='ml_moderation_model.joblib'):
    dump(model, path)

def load_model(path='ml_moderation_model.joblib'):
    return load(path)

# Example usage:
if __name__ == '__main__':
    X, y = load_data('moderation_reviews.csv')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = train_model(X_train, y_train)
    evaluate_model(model, X_test, y_test)
    save_model(model)