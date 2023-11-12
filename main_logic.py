import json
from search_sustainabilty import search_sustainabilty
from search_companies_with_sustenability import search_companies_with_sustenability
from poll_api import get_pollution_data
from dummy_script import company_profile
from credit_score import credit_score
from seismic_risk import get_seismic_risk

show_flag = False

def match_and_enrich(name, website):
	company_json = json.loads(company_profile(name, website))
	metadata = {}
	metadata["name"] = company_json["company_commercial_names"][0]
	metadata["website"] = website
	metadata["main_business_category"] = company_json["main_business_category"]
	metadata["employee_count"] = company_json["employee_count"]
	metadata["estimated_revenue"] = company_json["estimated_revenue"]
	metadata["locations"] = []
	metadata["main_country"] = company_json["main_country"]
	total_aqi = 0.0
	len_aqi = 0.0

	scores = []
	for location in company_json["locations"]:
		location_metadata = {}
		location_metadata["region"] = location["region"]
		location_metadata["city"] = location["city"]
		latitude = location["latitude"]
		longitude = location["longitude"]
		pollution_metadata = json.loads(get_pollution_data(latitude, longitude))
		aqi = pollution_metadata["aqi"]
		total_aqi += aqi
		len_aqi += 1.0
		location_metadata["aqi"] = aqi
		location_metadata["air_category"] = pollution_metadata["category"]
		location_metadata["pollutants"] = []
		for pollutant in pollution_metadata["pollutants"]:
			location_metadata["pollutants"].append({"name": pollutant["fullName"], "concentration": pollutant["concentration"]})
		
		sustainabily = search_sustainabilty(website)
		seismic_mag, seismic_sig = json.loads(get_seismic_risk(latitude, longitude))["seismic_risk_factor"]
		location_metadata["seismic"] = [seismic_mag, seismic_sig]
		score = credit_score(aqi, seismic_mag, sustainabily, num_employees=company_json["employee_count"], num_locations=company_json["num_locations"], estimated_revenue=company_json["estimated_revenue"])
		scores.append(score)
		metadata["locations"].append(location_metadata)
	
	# mean of scores with 2 decimal places
	metadata["credit_score"] = round(sum(scores) / len(scores), 2)
	metadata["average_aqi"] = round(total_aqi / len_aqi, 2)
	print(metadata)
