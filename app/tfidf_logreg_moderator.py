import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from joblib import dump
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

# Ensure NLTK resources are downloaded
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

def preprocess(text):
    """Lowercase, remove stopwords, and simple cleaning."""
    words = [word for word in text.lower().split() if word.isalpha() and word not in STOPWORDS]
    return ' '.join(words)

def load_data(csv_path):
    """Load labeled reviews from CSV, expects 'text' and 'label' columns."""
    df = pd.read_csv(csv_path)
    return df['text'], df['label']

def build_pipeline():
    """Constructs and returns the ML pipeline."""
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(preprocessor=preprocess)),
        ('clf', LogisticRegression(max_iter=1000, class_weight='balanced'))
    ])
    return pipeline

def train_and_evaluate(X_train, y_train, X_val, y_val):
    """Train pipeline and print evaluation metrics."""
    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_val)
    print("Validation set performance:")
    print(classification_report(y_val, preds))
    labels = ["clean", "profanity", "spam"]
    cm = confusion_matrix(y_val, preds, labels=labels)
    print("Confusion matrix for the Validation set:")
    print(cm)
    # Pretty plot
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap='Blues')
    plt.show(block=True)
    plt.savefig('confusion_matrix_val.png')
    print("Confusion matrix plot saved as confusion_matrix_val.png")
    return pipeline

def test_and_report(model, X_test, y_test):
    """Evaluate the trained model on the test set and print metrics."""
    preds = model.predict(X_test)
    print("Test set performance:")
    print(classification_report(y_test, preds))
    labels = ["clean", "profanity", "spam"]
    cm = confusion_matrix(y_test, preds, labels=labels)
    print("Confusion matrix for the Test set:")
    print(cm)
    # Pretty plot
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap='Blues')
    plt.show(block=True)
    plt.savefig('confusion_matrix_test.png')
    print("Confusion matrix plot saved as confusion_matrix_test.png")

def save_model(model, output_path):
    """Save the trained model to disk."""
    dump(model, output_path)
    print(f"Model saved to {output_path}")

def main():
    train_path = 'merged_train.csv'
    val_path = 'merged_val.csv'
    test_path = 'merged_test.csv'
    output_path = 'app/ml_moderation_model.joblib'

    X_train, y_train = load_data(train_path)
    X_val, y_val = load_data(val_path)
    X_test, y_test = load_data(test_path)

    model = train_and_evaluate(X_train, y_train, X_val, y_val)
    save_model(model, output_path)
    test_and_report(model, X_test, y_test)


if __name__ == '__main__':
    main()