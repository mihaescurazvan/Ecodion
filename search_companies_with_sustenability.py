import requests
import json

veridion_search_query_api_key = (
    "api-key"
)

def search_companies_with_sustenability():
    url = "https://data.veridion.com/search/v2/companies"

    headers = {
        "x-api-key": veridion_search_query_api_key,
        "Content-type": "application/json",
    }

    search_filters = {
        "filters": {
            "and": [
                {
                    "attribute": "company_industry",
                    "relation": "equals",
                    "value": "Manufacturing & Wholesale"
                }
                , 
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
                            "carbon reduction",
                            # Carbon Reduction
                            "Carbon footprint reduction",
                            "Carbon neutrality",
                            "Carbon offset",
                            "Low carbon initiatives",

                            # Renewable Energy
                            "Renewable energy sources",
                            "Green energy",
                            "Clean energy solutions",
                            "Sustainable energy practices",

                            # Resource Efficiency
                            "Resource conservation",
                            "Efficient resource utilization",
                            "Waste reduction",
                            "Circular economy practices",

                            # Environmental Impact
                            "Environmental stewardship",
                            "Reduced environmental impact",
                            "Eco-friendly practices",
                            "Biodiversity conservation",

                            # Sustainable Practices
                            "Sustainable development",
                            "Sustainable business practices",
                            "Ethical sourcing",
                            "Responsible production",

                            # Corporate Social Responsibility (CSR)
                            "CSR initiatives",
                            "Social and environmental responsibility",
                            "Social impact programs",
                            "Community engagement",

                            # Green Innovation
                            "Green technologies",
                            "Innovation for sustainability",
                            "Sustainable product development",
                            "Eco-friendly innovations",

                            # Water Conservation
                            "Water efficiency",
                            "Water conservation practices",
                            "Responsible water usage",

                            # Climate Action
                            "Climate change mitigation",
                            "Climate resilience",
                            "Adaptation strategies",

                            # Certifications and Standards
                            "LEED (Leadership in Energy and Environmental Design)",
                            "ISO 14001 (Environmental Management System)",
                            "B Corp certification",
                            "Fair Trade certification",

                            # Supply Chain Sustainability
                            "Sustainable supply chain",
                            "Responsible sourcing",
                            "Ethical supply chain practices",

                            # Employee Engagement
                            "Employee sustainability programs",
                            "Green employee initiatives",
                            "Sustainability training"
                        ]
                        }
                    }
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=search_filters)

    json_response = response.json()
    
    with open("company_info.json", "w", encoding="utf-8") as json_file:
        json.dump(json_response, json_file, ensure_ascii=False, indent=4)
    list_companies = []
    print(json_response["count"])
    for company in json_response["result"]:
        if company["employee_count"] != None:
            list_companies.append((company["company_name"], company["website_url"], company["employee_count"]))
    
    # sort list descending by number of employees, igoring the None values
    list_companies.sort(key=lambda tup: tup[2], reverse=True)
    return list_companies
    
