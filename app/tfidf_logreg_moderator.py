from app.text_preprocessing import preprocess
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from joblib import dump
import matplotlib.pyplot as plt


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
    val_report = classification_report(y_val, preds, target_names=["clean", "profanity", "spam"])
    print(val_report)
    # Save validation classification report as text file
    with open("classification_report_val_tfidf_logreg.txt", "w") as f:
        f.write(val_report)
    print("Validation classification report saved as classification_report_val_tfidf_logreg.txt")
    labels = ["clean", "profanity", "spam"]
    cm = confusion_matrix(y_val, preds, labels=labels)
    print("Confusion matrix for the Validation set:")
    print(cm)
    # Pretty plot
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap='Blues')
    plt.show(block=True)
    plt.savefig('confusion_matrix_val_tfidf_logreg.png')
    print("Confusion matrix plot saved as confusion_matrix_val_tfidf_logreg.png")
    return pipeline

def test_and_report(model, X_test, y_test):
    """Evaluate the trained model on the test set and print metrics."""
    preds = model.predict(X_test)
    print("Test set performance:")
    test_report = classification_report(y_test, preds, target_names=["clean", "profanity", "spam"])
    print(test_report)
    # Save test classification report as text file
    with open("classification_report_test_tfidf_logreg.txt", "w") as f:
        f.write(test_report)
    print("Test classification report saved as classification_report_test_tfidf_logreg.txt")
    labels = ["clean", "profanity", "spam"]
    cm = confusion_matrix(y_test, preds, labels=labels)
    print("Confusion matrix for the Test set:")
    print(cm)
    # Pretty plot
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap='Blues')
    plt.show(block=True)
    plt.savefig('confusion_matrix_test_tfidf_logreg.png')
    print("Confusion matrix plot saved as confusion_matrix_test_tfidf_logreg.png")

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
