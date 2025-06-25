import pandas as pd
import logging
import argparse
import sys

def merge_and_save(jigsaw_file, youtube_file, out_file):
    """
    Merge two files (Jigsaw and YouTube split) and write merged output.
    """
    try:
        # Load Jigsaw and YouTube split files
        jigsaw = pd.read_csv(jigsaw_file)
        youtube = pd.read_csv(youtube_file)

        # Concatenate the two DataFrames
        merged = pd.concat([jigsaw, youtube], ignore_index=True)

        # Save the merged split to disk
        merged.to_csv(out_file, index=False)
        logging.info(f"Saved: {out_file} ({len(merged)} rows)")
    except Exception as e:
        logging.error(f"Failed to merge {jigsaw_file} and {youtube_file}: {e}")
        sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(description="Merge Jigsaw and YouTube data splits.")
    parser.add_argument('--splits', nargs='+', default=['train', 'val', 'test'],
                        help="List of split names to merge (default: train val test)")
    parser.add_argument('--jigsaw_prefix', default='jigsaw_',
                        help="Prefix for Jigsaw files (default: jigsaw_)")
    parser.add_argument('--youtube_prefix', default='youtube_',
                        help="Prefix for YouTube files (default: youtube_)")
    parser.add_argument('--output_prefix', default='merged_',
                        help="Prefix for output files (default: merged_)")
    parser.add_argument('--suffix', default='.csv',
                        help="File suffix (default: .csv)")
    return parser.parse_args()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')
    args = parse_args()
    for split in args.splits:
        jigsaw_file = f'{args.jigsaw_prefix}{split}{args.suffix}'
        youtube_file = f'{args.youtube_prefix}{split}{args.suffix}'
        out_file = f'{args.output_prefix}{split}{args.suffix}'
        merge_and_save(jigsaw_file, youtube_file, out_file)