import math


def credit_score(air_quality, seismic_risk, sustainability, num_employees=None, num_locations=None, estimated_revenue=None):
    # Normalizing air quality and seismic risk to be between 0 and 1
    normalized_air_quality = air_quality / 100.0  # Assuming air quality is given as a percentage
    normalized_seismic_risk = seismic_risk / 9.5  # Assuming seismic risk is given on a scale of 1 to 4

    # Weights for different factors
    w_air_quality = 0.35
    w_seismic_risk = 0.25
    w_sustainability = 0.25
    w_employees = 0.05
    w_locations = 0.05
    w_revenue = 0.05

    # Scoring function
    score = (
        w_air_quality * math.log1p(1 + normalized_air_quality) +
        w_seismic_risk * (1 - normalized_seismic_risk / 5) +
        w_sustainability * sustainability +
        w_employees * (0 if num_employees is None else math.log1p(1 + num_employees)) +
        w_locations * (0 if num_locations is None else math.log1p(1 + num_locations)) +
        w_revenue * (0 if estimated_revenue is None else math.log1p(1 + estimated_revenue))
    )

    # Convert the score to a percentage (between 0 and 100)
    score_percentage = 100 / (1 + math.exp(-score))

    return score_percentage