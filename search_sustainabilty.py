import requests
import json

veridion_search_query_api_key = (
    "api-key"
)

def search_sustainabilty(website):
    url = "https://data.veridion.com/search/v2/companies"

    headers = {
        "x-api-key": veridion_search_query_api_key,
        "Content-type": "application/json",
    }

    search_filters = {
        "filters": {
            "and": [
                {
                    "attribute": "company_website",
                    "relation": "equals",
                    "value": website
                },
                {
                    "attribute": "company_keywords",
                    "relation": "match_expression",
                    "value": {
                        "match": {
                        "operator": "or",
                        "operands": [
                            "Sustainability",
                            "ESG Compliance",
                            "Environmental Social Governance",
                            "Environmental & Social",
                            "Environmental Stewardship",
                            "Environmental Management",
                            "Sustainable business",
                            "co2",
                            "renewable energies",
                            "emissions",
                            "carbon",
                            "Renewable",

                            # Resource Efficiency
                            "Resource conservation",
                            "Efficient resource utilization",
                            "Waste reduction",
                            "Circular economy practices",

                            # Environmental Impact
                            "Environmental",
                            "Eco-friendly",
                            "Biodiversity",

                            # Sustainable Practices
                            "Sustainable",
                            "Ethical sourcing",
                            "production",

                            # Corporate Social Responsibility (CSR)
                            "CSR initiatives",
                            "Social and environmental responsibility",
                            "Social impact programs",
                            "Community engagement",

                            # Green Innovation
                            "Green",
                            "LEED",
                            "ISO 14001 (Environmental Management System)",
                            "B Corp certification",
                            "Fair Trade certification",
                            "Ethical",
                        ]
                        }
                    }
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=search_filters)

    json_response = response.json()
    
    return json_response["count"]
