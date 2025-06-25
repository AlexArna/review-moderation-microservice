#!/usr/bin/env python3
import pandas as pd
import re
import logging
import sys
import argparse

abuse_columns = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']

def normalize_text(text):
    """Normalize repeated punctuation, characters, and emojis."""
    # Limit repeated punctuation (e.g., '!!!' -> '!')
    text = re.sub(r'([!?.])\1{1,}', r'\1', text)
    # Limit repeated characters (e.g., 'cooool' -> 'cool')
    text = re.sub(r'(.)\1{2,}', r'\1\1', text)
    # Limit repeated emojis (for most emojis)
    text = re.sub(r'([\U00010000-\U0010ffff])\1{1,}', r'\1', text)
    return text

def preprocess(df, text_col, label_cols):
    """Cleans and normalizes the dataframe, assigns labels."""
    # Drop rows with empty text
    df = df[df[text_col].notnull() & (df[text_col].str.strip() != '')].copy()
    # Normalize text
    df['text'] = df[text_col].apply(normalize_text).astype(str)
    # Assign label
    df['label'] = df[label_cols].astype(str).eq('1').any(axis=1).map({True: 'profanity', False: 'clean'})
    return df[['text', 'label']]

def process_train_val(train_path='train.csv'):
    """Process the train.csv file, shuffle, split, and save train/val sets."""
    try:
        logging.info(f"Reading {train_path}...")
        train_df = pd.read_csv(train_path)
        df = preprocess(train_df, 'comment_text', abuse_columns)
        df = df.sample(frac=1, random_state=41).reset_index(drop=True)  # Shuffle
        split = int(len(df) * 0.8)
        df.iloc[:split].to_csv('jigsaw_train.csv', index=False)  # First 80% rows for training
        df.iloc[split:].to_csv('jigsaw_val.csv', index=False)
        logging.info(f"Saved jigsaw_train.csv ({split} rows) and jigsaw_val.csv ({len(df) - split} rows).")
    except Exception as e:
        logging.error(f"Error processing train/val: {e}")
        raise

def process_test(test_path='test.csv', test_labels_path='test_labels.csv'):
    """Process the test and test_labels CSVs, filter, and save test set."""
    try:
        logging.info(f"Reading {test_path} and {test_labels_path}...")
        test_df = pd.read_csv(test_path)
        test_labels_df = pd.read_csv(test_labels_path)
        test_full = pd.merge(test_df, test_labels_df, on='id')
        # Filter out rows where any abuse column == -1
        test_full = test_full[(test_full[abuse_columns] != -1).all(axis=1)]
        test_processed = preprocess(test_full, 'comment_text', abuse_columns)
        test_processed.to_csv('jigsaw_test.csv', index=False)
        logging.info(f"Saved jigsaw_test.csv ({len(test_processed)} rows).")
    except Exception as e:
        logging.error(f"Error processing test: {e}")
        raise

def parse_args():
    parser = argparse.ArgumentParser(description="Preprocess the Jigsaw toxic comment dataset for classification.")
    parser.add_argument('--train_csv', default='train.csv', help='Path to train.csv')
    parser.add_argument('--test_csv', default='test.csv', help='Path to test.csv')
    parser.add_argument('--test_labels_csv', default='test_labels.csv', help='Path to test_labels.csv')
    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    args = parse_args()
    try:
        process_train_val(train_path=args.train_csv)
        process_test(test_path=args.test_csv, test_labels_path=args.test_labels_csv)
        logging.info("Preprocessing completed successfully.")
    except Exception:
        logging.error("Preprocessing failed.", exc_info=True)
        sys.exit(1)