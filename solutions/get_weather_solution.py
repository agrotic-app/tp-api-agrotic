import requests

# Base URL for Open-Meteo API
url = "https://api.open-meteo.com/v1/forecast"

# Parameters for Montpellier (latitude, longitude) and desired data
params = {
    "latitude": 43.6119,
    "longitude": 3.8772,
    "current_weather": "true",
    "daily": "precipitation_sum",
    "timezone": "Europe/Paris"
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code != 200:
    print(f"Erreur API : Code {response.status_code}")
    exit(1)

data = response.json()

# Extract temperature and precipitation with error handling
temperature = data.get('current_weather', {}).get('temperature', 'N/A')
precipitation = data.get('daily', {}).get('precipitation_sum', [0])[0]

print(f"Température actuelle : {temperature}°C")
print(f"Cumul de précipitation journalier : {precipitation} mm")