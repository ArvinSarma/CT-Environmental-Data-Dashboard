import pandas as pd
import os
from sodapy import Socrata
from dotenv import load_dotenv


load_dotenv()

# Example authenticated client (needed for non-public datasets):
def get_data(datasetId, limitNum, fileName):
    ctgov_api = os.getenv("CTGOV_API")
    print(ctgov_api)
    
    client = Socrata('data.ct.gov',
                    ctgov_api)

    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get(datasetId, limit=limitNum)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df.to_csv(fileName, index= False)
