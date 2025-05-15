#!/usr/bin/env python3

import os
import sys
import logging
from pathlib import Path
import pandas as pd

# Configure logging
logging.basicConfig(
    filename='sync.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
POSTING_DIR = Path.home() / "Desktop" / "Posting"
EXCEL_FILE = POSTING_DIR / "контент планчик.xlsx"
TAG_NAME = "twitter done"

def read_excel_data():
    """Read data from the Excel file."""
    try:
        # Read the Excel file
        df = pd.read_excel(EXCEL_FILE, sheet_name="Лист1")
        # Convert to list of lists (similar to the previous Google Sheets format)
        return df.values.tolist()
    except Exception as e:
        logging.error(f"Failed to read Excel file: {e}")
        sys.exit(1)

def tag_file(file_path):
    """Add 'twitter done' tag to file using the 'tag' command."""
    try:
        # Check if tag already exists
        result = os.system(f'tag -l "{file_path}" | grep -q "{TAG_NAME}"')
        if result == 0:
            return True  # Tag already exists
        
        # Add tag
        result = os.system(f'tag -a "{TAG_NAME}" "{file_path}"')
        return result == 0
    except Exception as e:
        logging.error(f"Failed to tag file {file_path}: {e}")
        return False

def remove_tag(file_path):
    """Remove 'twitter done' tag from file using the 'tag' command."""
    try:
        # Check if tag exists
        result = os.system(f'tag -l "{file_path}" | grep -q "{TAG_NAME}"')
        if result != 0:
            return True  # Tag doesn't exist, so nothing to remove
        
        # Remove tag
        result = os.system(f'tag -r "{TAG_NAME}" "{file_path}"')
        return result == 0
    except Exception as e:
        logging.error(f"Failed to remove tag from file {file_path}: {e}")
        return False

def process_row(row):
    """Process a single row from the Excel file."""
    file_id = str(int(row[0]))  # Column A - convert to integer to remove decimal points
    date = row[2]      # Column C - twi column
    
    # Look for file in Posting directory
    posting_dir = Path(POSTING_DIR)
    if not posting_dir.exists():
        logging.error(f"Posting directory not found: {POSTING_DIR}")
        return
    
    # Find files that start with the ID number
    matching_files = []
    for ext in ['.jpg', '.png']:
        pattern = f"{file_id}{ext}"
        matching_files.extend(posting_dir.glob(pattern))
    
    if not matching_files:
        logging.info(f"skipped—no file: {file_id}")
        return
    
    # Check if date is valid (not NaT, None, or empty string)
    if pd.isna(date) or str(date).strip() == '':
        # Remove tag from all matching files
        for file_path in matching_files:
            if remove_tag(file_path):
                logging.info(f"removed tag from: {file_path.name}")
            else:
                logging.error(f"✗ error: Failed to remove tag from {file_path.name}")
        return
    
    # Process each matching file - add tag if date is valid
    for file_path in matching_files:
        if tag_file(file_path):
            logging.info(f"✓ {file_path.name}")
        else:
            logging.error(f"✗ error: Failed to tag {file_path.name}")

def main():
    """Main execution function."""
    # Check if Excel file exists
    if not EXCEL_FILE.exists():
        logging.error(f"Excel file not found: {EXCEL_FILE}")
        sys.exit(1)
    
    # Read and process rows
    rows = read_excel_data()
    for row in rows[1:]:  # Skip header row
        process_row(row)

if __name__ == "__main__":
    main() 