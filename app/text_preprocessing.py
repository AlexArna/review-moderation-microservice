import nltk
from nltk.corpus import stopwords

# Ensure NLTK resources are downloaded
nltk.download('stopwords')
STOPWORDS = set(stopwords.words('english'))

def preprocess(text):
    """Lowercase, remove stopwords, and simple cleaning."""
    words = [word for word in text.lower().split() if word.isalpha() and word not in STOPWORDS]
    return ' '.join(words)