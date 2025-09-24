import requests

# Base URL for Open-Meteo API
url = "https://api.open-meteo.com/v1/forecast"

# TODO: Exercise 1 - Construct the API request parameters
# 1. Add parameters to the 'params' dictionary to fetch:
#    - Current weather data
#    - Daily precipitation sum
#    - Timezone set to Europe/Paris
# 2. Refer to the Open-Meteo documentation: https://open-meteo.com/en/docs
# Example: params = {"latitude": 43.6119, "longitude": 3.8772, ...}
params = {}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code != 200:
    print(f"API Error: Status code {response.status_code}")
    exit(1)

data = response.json()

# TODO: Exercise 2 - Extract temperature and precipitation
# 1. Extract current temperature from data['current_weather']['temperature']
# 2. Extract daily precipitation sum from data['daily']['precipitation_sum'][0]
# 3. Add error handling to check if these keys exist in the response
# Example: Use data.get('key', default) or try-except to avoid KeyError
temperature = None  # Your code here
precipitation = None  # Your code here

print(f"Current temperature: {temperature}°C")
print(f"Daily precipitation sum: {precipitation} mm")