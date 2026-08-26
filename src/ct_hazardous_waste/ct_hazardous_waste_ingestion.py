#!/usr/bin/env python


import pandas as pd
from sodapy import Socrata

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
#client = Socrata("data.ct.gov", None)

# Example authenticated client (needed for non-public datasets):
client = Socrata('data.ct.gov',
                 'gekvcHEnVThIovuEOppkZZjjy')

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("x2z6-swxe", limit=2000000)

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
results_df.to_csv("data/Hazardous_waste.csv", index= False)