#!/usr/bin/env python3

import os
import sys
import logging
import pandas as pd
from pathlib import Path
import time
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    filename='auto_tag_manager.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
POSTING_DIR = Path.home() / "Desktop" / "Posting"
EXCEL_FILE = POSTING_DIR / "контент планчик.xlsx"
TAGS = {
    'twi': "free for twi",
    'inst': "free for inst"
}
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']

def manage_tag(file_path, tag_name, should_have_tag):
    """Add or remove a tag based on whether the file should have it."""
    try:
        # Get current tags
        current_tags = os.popen(f'tag -l "{file_path}"').read().strip()
        has_tag = tag_name in current_tags

        if should_have_tag and not has_tag:
            # Add tag if it should have it but doesn't
            result = os.system(f'tag -a "{tag_name}" "{file_path}"')
            if result == 0:
                logging.info(f"Added tag {tag_name} to: {file_path.name}")
            else:
                logging.error(f"Failed to add tag {tag_name} to: {file_path.name}")
        elif not should_have_tag and has_tag:
            # Remove tag if it shouldn't have it but does
            result = os.system(f'tag -r "{tag_name}" "{file_path}"')
            if result == 0:
                logging.info(f"Removed tag {tag_name} from: {file_path.name}")
            else:
                logging.error(f"Failed to remove tag {tag_name} from: {file_path.name}")
        
        return True
    except Exception as e:
        logging.error(f"Error managing tag {tag_name} for file {file_path}: {e}")
        return False

def process_row(row):
    """Process a single row from the Excel file."""
    try:
        # Get the ID and dates from the row
        file_id = str(int(row[0]))  # Convert to integer to remove decimal points
        twi_date = row[2]  # twi column
        inst_date = row[3]  # inst column
        
        # Find matching files
        matching_files = []
        for ext in IMAGE_EXTENSIONS:
            file_path = POSTING_DIR / f"{file_id}{ext}"
            if file_path.exists():
                matching_files.append(file_path)
        
        # Process each matching file
        for file_path in matching_files:
            # Check twi tag
            should_have_twi_tag = pd.isna(twi_date) or not str(twi_date).strip()
            manage_tag(file_path, TAGS['twi'], should_have_twi_tag)
            
            # Check inst tag
            should_have_inst_tag = pd.isna(inst_date) or not str(inst_date).strip()
            manage_tag(file_path, TAGS['inst'], should_have_inst_tag)
                
    except Exception as e:
        logging.error(f"Error processing row {row}: {e}")

def process_files():
    """Process all files in the Excel sheet."""
    try:
        # Check if Posting directory exists
        if not POSTING_DIR.exists():
            logging.error(f"Posting directory not found: {POSTING_DIR}")
            return False
        
        # Check if Excel file exists
        if not EXCEL_FILE.exists():
            logging.error(f"Excel file not found: {EXCEL_FILE}")
            return False
        
        # Read the Excel file
        df = pd.read_excel(EXCEL_FILE)
        
        # Process each row
        for _, row in df.iterrows():
            process_row(row)
            
        return True
            
    except Exception as e:
        logging.error(f"Error processing files: {e}")
        return False

def main():
    """Main execution function that runs every 2 days."""
    logging.info("Starting auto tag manager")
    
    while True:
        try:
            logging.info("Starting new processing cycle")
            process_files()
            logging.info("Processing cycle completed")
            
            # Wait for 2 days
            time.sleep(2 * 24 * 60 * 60)  # 2 days in seconds
            
        except KeyboardInterrupt:
            logging.info("Script stopped by user")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            # Wait for 1 hour before retrying if there's an error
            time.sleep(60 * 60)

if __name__ == "__main__":
    main() 