#!/usr/bin/env python3

import os
import sys
import logging
import pandas as pd
from pathlib import Path

# Configure logging
logging.basicConfig(
    filename='free_for_twi.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
POSTING_DIR = Path.home() / "Desktop" / "Posting"
EXCEL_FILE = POSTING_DIR / "контент планчик.xlsx"
TAG_NAME = "free for twi"

def add_tag(file_path):
    """Add the 'free for twi' tag to a file using the 'tag' command."""
    try:
        # Check if the file already has the tag
        result = os.popen(f'tag -l "{file_path}"').read().strip()
        if TAG_NAME in result:
            return True  # Tag already present
        
        # Add the tag
        result = os.system(f'tag -a "{TAG_NAME}" "{file_path}"')
        return result == 0
    except Exception as e:
        logging.error(f"Failed to add tag to file {file_path}: {e}")
        return False

def process_row(row):
    """Process a single row from the Excel file."""
    try:
        # Get the ID and date from the row
        file_id = str(int(row[0]))  # Convert to integer to remove decimal points
        date = row[2]  # twi column
        
        # Skip if there's a valid date
        if not pd.isna(date) and str(date).strip():
            return
        
        # Find matching files
        matching_files = []
        for ext in ['.jpg', '.png']:
            file_path = POSTING_DIR / f"{file_id}{ext}"
            if file_path.exists():
                matching_files.append(file_path)
        
        # Tag all matching files
        for file_path in matching_files:
            if add_tag(file_path):
                logging.info(f"Added tag to: {file_path.name}")
            else:
                logging.error(f"Failed to add tag to: {file_path.name}")
                
    except Exception as e:
        logging.error(f"Error processing row {row}: {e}")

def main():
    """Main execution function."""
    # Check if Posting directory exists
    if not POSTING_DIR.exists():
        logging.error(f"Posting directory not found: {POSTING_DIR}")
        sys.exit(1)
    
    # Check if Excel file exists
    if not EXCEL_FILE.exists():
        logging.error(f"Excel file not found: {EXCEL_FILE}")
        sys.exit(1)
    
    try:
        # Read the Excel file
        df = pd.read_excel(EXCEL_FILE)
        
        # Process each row
        for _, row in df.iterrows():
            process_row(row)
            
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 