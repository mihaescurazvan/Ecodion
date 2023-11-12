import json
import requests
from datetime import datetime, timedelta
from time import sleep


def get_seismic_risk(latitude, longitude):
    # Define the base URL of the USGS API
    base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'

    # Define the time range for the past 30 days
    end_time = datetime.utcnow()  # Current date and time
    start_time = end_time - timedelta(days=3650)  # 90 days ago

    # Format the time strings according to the API requirements
    start_time_str = start_time.strftime("%Y-%m-%dT%H:%M:%S")
    end_time_str = end_time.strftime("%Y-%m-%dT%H:%M:%S")

    # Set parameters for the API request
    payload = {
        'format': 'geojson',  # Response format as JSON
        'latitude': latitude,
        'longitude': longitude,
        'maxradiuskm': 30,
        'starttime': start_time_str,
        'endtime': end_time_str
    }

    # Make the API request
    json_request = requests.get(base_url, params=payload)
    sleep(1)

    json_response = json_request.json()
    
    seismic_data = {}
    seismic_data['count'] = json_response['metadata']['count']
    seismic_data['events'] = []
    total_magnitude = 0.0
    total_sig = 0.0

    for feature in json_response['features']:
        if (feature["properties"]["mag"] is None) or (feature["properties"]["sig"] is None):
            continue
        total_magnitude += (feature["properties"]["mag"])/1.0
        total_sig += feature["properties"]["sig"]/1.0
        event = {
            "time": datetime.utcfromtimestamp(((float)(feature["properties"]["time"])/1000)).strftime('%Y-%m-%d %H:%M:%S'),
            "tsunami": feature["properties"]["tsunami"],
            "sig": feature["properties"]["sig"],
            "type": feature["properties"]["type"],
        }
        seismic_data['events'].append(event)

    if total_magnitude > 0.0:
        total_magnitude /= (seismic_data['count']/1.0)
        total_sig /= (seismic_data['count']/1.0)
    
    seismic_data['seismic_risk_factor'] = total_magnitude, total_sig

    return json.dumps(seismic_data, ensure_ascii=False).encode('utf-8')
    
