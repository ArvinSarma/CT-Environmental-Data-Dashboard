import requests
import json

# Define the target URL for creating the replica
url = "https://services8.arcgis.com/vfliU0HxOrbPHYI9/arcgis/rest/services/ct_towns/FeatureServer/createReplica"

# Define the payload parameters for the POST request
# Adjust layerQueries, geometry, or replicaName based on your specific requirements
payload = {
    'f': 'json',
    'replicaName': 'ct_towns',
    'layers': '0',  # Specifies the layer ID(s) to include
    'layerQueries': '',
    'geometry': '',
    'geometryType': 'esriGeometryEnvelope',
    'inSR': '',
    'replicaSR': '',
    'transportType': 'esriTransportTypeUrl',
    'returnAttachments': 'true',
    'returnAttachmentsDataByUrl': 'false',
    'async': 'false',  # Set to true if the dataset is massive and requires polling
    'syncModel': 'none',
    'dataFormat': 'csv',  # Options include 'json', 'sqlite', or 'filegdb'
    'replicaOptions': ''
}

print("Sending POST request to create replica...")

try:
    # Execute the POST request
    response = requests.post(url, data=payload)
    response.raise_for_status()

    # Parse the response JSON
    response_data = response.json()
    print(response_data)

    # Check if the response contains direct data or a download URL
    if 'responseUrl' in response_data:
        download_url = response_data['responseUrl']
        print(f"Replica created successfully. Downloading data from: {download_url}")

        # Download the actual data file
        file_response = requests.get(download_url)
        file_response.raise_for_status()

        # Save the file (adjust extension based on your dataFormat, e.g., .zip for filegdb/sqlite)
        output_file = "data/CT_Towns.csv"
        with open(output_file, "wb") as f:
            f.write(file_response.content)
        print(f"Dataset downloaded successfully and saved to {output_file}")

    elif 'replicaID' in response_data:
        # If the response returns raw data instead of a URL
        output_file = "CT_Towns.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(response_data, f, indent=4)
        print(f"Replica data saved directly to {output_file}")

    else:
        # Handle cases where the server returns an explicit ArcGIS error
        if 'error' in response_data:
            print(f"ArcGIS Server Error: {response_data['error'].get('message')}")
        else:
            print("Unexpected response structure. Saving raw response to debug.json")
            with open("debug.json", "w", encoding="utf-8") as f:
                json.dump(response_data, f, indent=4)

except requests.exceptions.RequestException as e:
    print(f"HTTP Request failed: {e}")
except json.JSONDecodeError:
    print("Failed to decode JSON from the server response.")
