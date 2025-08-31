# List of Indian coastal cities (major ones)
COASTAL_CITIES = [
    "Mumbai", "Chennai", "Kolkata", "Visakhapatnam", "Kochi", "Mangalore",
    "Thiruvananthapuram", "Panaji", "Puducherry", "Kakinada", "Tuticorin",
    "Nagapattinam", "Cuddalore", "Veraval", "Porbandar", "Bhavnagar",
    "Jamnagar", "Kandla", "Okha", "Dwarka", "Bet Dwarka", "Daman", "Diu",
    "Rameswaram", "Pamban"
]

def check_risk(wind_speed, tide_level, rainfall):
    """
    Determine alert level and message based on weather parameters.
    Thresholds:
    - RED: High wind (>50 km/h), high tide (>4m), heavy rain (>50mm)
    - ORANGE: Moderate wind (>30 km/h), moderate tide (>3m), moderate rain (>20mm)
    - YELLOW: Low wind (>15 km/h), low tide (>2m), light rain (>10mm)
    - GREEN: Safe conditions
    """
    if wind_speed > 50 or tide_level > 4 or rainfall > 50:
        level = "RED"
        message = "Extreme weather conditions detected. Evacuate immediately if in coastal area."
    elif wind_speed > 30 or tide_level > 3 or rainfall > 20:
        level = "ORANGE"
        message = "High risk of flooding or strong winds. Prepare emergency kits and stay alert."
    elif wind_speed > 15 or tide_level > 2 or rainfall > 10:
        level = "YELLOW"
        message = "Moderate weather activity. Monitor conditions closely."
    else:
        level = "GREEN"
        message = "Weather conditions are safe."

    return level, message
