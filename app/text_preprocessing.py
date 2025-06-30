import nltk
from nltk.corpus import stopwords

# Only download NLTK resources if not already downloaded
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

STOPWORDS = set(stopwords.words('english'))

def preprocess(text):
    """Lowercase, remove stopwords, and simple cleaning."""
    words = [word for word in text.lower().split() if word.isalpha() and word not in STOPWORDS]
    return ' '.join(words)