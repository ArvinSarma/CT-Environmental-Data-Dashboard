import os
import sys
from ct_data.get_ctgov_data import get_data

RECORD_LIMIT = 2000000

def extract_data(filepath):
    output_filename = "Hazardous_waste.csv"
    full_filename = os.path.join(filepath, output_filename)
    get_data("x2z6-swxe", RECORD_LIMIT, full_filename)
    return full_filename

if __name__ == "__main__":
    SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(SRC_DIR)
    PROJECT_ROOT = os.path.dirname(SRC_DIR)
    OUTPUT_FILE = os.path.join(PROJECT_ROOT, "data")
    filename = extract_data(OUTPUT_FILE)
    print(f"Filename: {filename}")