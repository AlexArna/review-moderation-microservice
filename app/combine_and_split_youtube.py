import glob
import re
import pandas as pd

def normalize_text(text):
    """Normalize repeated punctuation, characters, and emojis."""
    # Limit repeated punctuation (e.g., '!!!' -> '!')
    text = re.sub(r'([!?.])\1{1,}', r'\1', text)
    # Limit repeated characters (e.g., 'cooool' -> 'cool')
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    # Limit repeated emojis (for most emojis)
    text = re.sub(r'([\U00010000-\U0010ffff])\1{1,}', r'\1', text)
    return text

def load_and_concat(files):
    """Load and concatenate Youtube CSV spam datasets."""
    dfs = []
    for fname in files:
        df = pd.read_csv(fname, usecols=['CONTENT', 'CLASS'])
        dfs.append(df)
    combined = pd.concat(dfs, ignore_index=True)
    return combined

def preprocess_youtube(df):
    """Cleans and normalizes the dataframe, assigns labels."""
    # Remove rows where CONTENT or CLASS is missing (NaN)
    df = df[df['CONTENT'].notnull() & df['CLASS'].notnull()]
    # Convert CONTENT and CLASS columns to string type
    df['CONTENT'] = df['CONTENT'].astype(str)
    df['CLASS'] = df['CLASS'].astype(str)
    # Remove rows where CONTENT and CLASS are empty (after stripping spaces)
    df = df[df['CONTENT'].str.strip() != '']
    df = df[df['CLASS'].str.strip() != '']
    # Normalize and map labels
    df['text'] = df['CONTENT'].apply(normalize_text)
    df['label'] = df['CLASS'].map(lambda x: 'spam' if x.strip() == '1' else ('clean' if x.strip() == '0' else None))
    # Drop rows where label mapping failed
    df = df[df['label'].notnull()]
    return df[['text', 'label']]

def split_and_save(df, train_frac=0.6, val_frac=0.2, seed=42):
    """Split into train/val/test and save as CSVs."""
    # Shuffling the rows to ensure randomness, setting seed for reproducibility
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    n = len(df)
    train_end = int(train_frac * n) # End index for train set (first 60%)
    val_end = int((train_frac + val_frac) * n) # End index for validation set (next 20%)
    df.iloc[:train_end].to_csv('youtube_train.csv', index=False)
    df.iloc[train_end:val_end].to_csv('youtube_val.csv', index=False)
    df.iloc[val_end:].to_csv('youtube_test.csv', index=False)

if __name__ == "__main__":
    input_files = glob.glob('Youtube*.csv')
    combined = load_and_concat(input_files)
    processed = preprocess_youtube(combined)
    processed.to_csv('youtube_spam_combined.csv', index=False)
    split_and_save(processed)
