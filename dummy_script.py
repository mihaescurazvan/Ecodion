veridion_match_enrich_api_key = (
    "api-key"
)
import requests
import json

def company_profile(company_name, website):
    url = "https://data.veridion.com/match/v4/companies"
    headers = {
        "x-api-key": veridion_match_enrich_api_key,
        "Content-type": "application/json",
    }

    data = {"commercial_names": [company_name], "website": website}

    response = requests.post(url, headers=headers, json=data)

    json_response = response.json()

    company_informations = {}
    company_informations["company_commercial_names"] = json_response[
        "company_commercial_names"
    ]
    company_informations["main_business_category"] = json_response[
        "main_business_category"
    ]


    locations = []
    for location in json_response["locations"]:
        if location["latitude"] and location["longitude"]:
            locations.append(location)

    company_informations["locations"] = locations
    company_informations["num_locations"] = json_response["num_locations"]
    company_informations["employee_count"] = json_response["employee_count"]
    company_informations["estimated_revenue"] = json_response["estimated_revenue"]
    company_informations["main_country"] = json_response["main_country"]


    return json.dumps(company_informations, ensure_ascii=False).encode("utf-8")
