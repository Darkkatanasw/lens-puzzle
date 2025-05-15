#!/usr/bin/env python3

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    filename='tag_removal.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
POSTING_DIR = Path.home() / "Desktop" / "Posting"
TAG_NAME = "twitter done"

def remove_all_tags(file_path):
    """Remove the 'twitter done' tag from a file using the 'tag' command."""
    try:
        # Check if the file has the specific tag
        result = os.popen(f'tag -l "{file_path}"').read().strip()
        if TAG_NAME not in result:
            return True  # Tag not present
        
        # Remove the specific tag
        result = os.system(f'tag -r "{TAG_NAME}" "{file_path}"')
        return result == 0
    except Exception as e:
        logging.error(f"Failed to remove tag from file {file_path}: {e}")
        return False

def main():
    """Main execution function."""
    # Check if Posting directory exists
    if not POSTING_DIR.exists():
        logging.error(f"Posting directory not found: {POSTING_DIR}")
        sys.exit(1)
    
    # Process all files in the directory
    for file_path in POSTING_DIR.glob('*'):
        if file_path.is_file():  # Only process files, not directories
            if remove_all_tags(file_path):
                logging.info(f"Removed tag from: {file_path.name}")
            else:
                logging.error(f"Failed to remove tag from: {file_path.name}")

if __name__ == "__main__":
    main() 