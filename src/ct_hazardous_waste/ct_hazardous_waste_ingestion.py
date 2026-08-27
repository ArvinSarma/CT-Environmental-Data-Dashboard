import os
import sys
from dotenv import load_dotenv

# 1. PATH SETUP
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SRC_DIR)

PROJECT_ROOT = os.path.dirname(SRC_DIR)

from get_ctgov_data import get_data
# Load the .env file
load_dotenv()
get_data("x2z6-swxe", 2000000, "Hazardous_waste")
