import os
import sys


# 1. PATH SETUP
SRC_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SRC_DIR)
from get_ctgov_data import get_data

PROJECT_ROOT = os.path.dirname(SRC_DIR)
CSV_PATH = os.path.join(PROJECT_ROOT,"data","Hazardous_waste.csv")



get_data("x2z6-swxe", 2000000, CSV_PATH)
