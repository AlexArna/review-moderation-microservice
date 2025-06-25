#!/usr/bin/env python3
import pandas as pd
import argparse
import logging

def load_data(path):
    """Load a CSV into a DataFrame."""
    try:
        df = pd.read_csv(path)
        logging.info(f"Loaded {path} ({len(df)} rows)")
        return df
    except Exception as e:
        logging.error(f"Failed to load {path}: {e}")
        raise

def print_label_distribution(df, label_col="label"):
    """Print the distribution and imbalance of the label column."""
    counts = df[label_col].value_counts()
    logging.info("Label distribution:\n" + str(counts))
    ratio = counts.max() / counts.min() if len(counts) > 1 else 1.0
    logging.info(f"Class imbalance ratio (max/min): {ratio:.2f}")

def print_text_stats(df, text_col="text"):
    """Print summary stats for text length."""
    text_lengths = df[text_col].astype(str).str.len()
    logging.info("Text length stats:")
    logging.info(text_lengths.describe().to_string())

def show_samples(df, label_col="label", text_col="text", n=2):
    """Show a few sample texts per class."""
    for label in df[label_col].unique():
        logging.info(f"\nSample texts for label '{label}':")
        samples = df[df[label_col] == label][text_col].head(n)
        for i, text in enumerate(samples, 1):
            logging.info(f"  {i}. {text[:100]}{'...' if len(text) > 100 else ''}")

def analyze_split(path, split_name):
    logging.info(f"\n==== {split_name.upper()} SET ====")
    df = load_data(path)
    logging.info(f"Total samples: {len(df)}")
    print_label_distribution(df)
    print_text_stats(df)
    show_samples(df)

def parse_args():
    parser = argparse.ArgumentParser(description="Explore dataset statistics for Jigsaw merged splits.")
    parser.add_argument('--train', default='merged_train.csv', help='Path to merged train CSV')
    parser.add_argument('--val', default='merged_val.csv', help='Path to merged val CSV')
    parser.add_argument('--test', default='merged_test.csv', help='Path to merged test CSV')
    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s'
    )
    args = parse_args()
    analyze_split(args.train, "train")
    analyze_split(args.val, "val")
    analyze_split(args.test, "test")