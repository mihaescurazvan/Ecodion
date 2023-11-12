google_api_key = "AIzaSyCfOM8_B51Sd7E4R53EHRQ6dmwWMO8ff-8"
import requests
import json


def get_pollution_data(latitude, longitude):
    url = (
        "https://airquality.googleapis.com/v1/currentConditions:lookup?key="
        + google_api_key
    )
    headers = {"Content-type": "application/json"}

    data = {
        "universalAqi": True,
        "location": {"latitude": latitude, "longitude": longitude},
        "extraComputations": [
            "HEALTH_RECOMMENDATIONS",
            "DOMINANT_POLLUTANT_CONCENTRATION",
            "POLLUTANT_CONCENTRATION",
            "POLLUTANT_ADDITIONAL_INFO",
        ],
    }

    response = requests.post(url, headers=headers, json=data)

    json_response = response.json()
    pollution_data = {}
    pollution_data["regionCode"] = json_response["regionCode"]
    pollution_data["aqi"] = json_response["indexes"][0]["aqi"]
    pollution_data["category"] = json_response["indexes"][0]["category"]
    pollution_data["dominantPollutant"] = json_response["indexes"][0][
        "dominantPollutant"
    ]

    pollutants = [
        {
            "fullName": pollutant["fullName"],
            "code": pollutant["code"],
            "concentration": pollutant["concentration"],
        }
        for pollutant in json_response["pollutants"]
    ]

    pollution_data["pollutants"] = pollutants

    return json.dumps(pollution_data, ensure_ascii=False).encode('utf-8')
