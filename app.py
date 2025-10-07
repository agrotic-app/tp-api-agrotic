from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Chichi forever !"

# TODO: Exercise 4 - Implement the irrigation advice endpoint
# 1. Create a route '/conseil-irrigation' that accepts 'lat' and 'lon' query parameters
# 2. Validate that 'lat' and 'lon' are provided and are valid numbers
# 3. Use requests.get() to fetch weather data from Open-Meteo API (reuse logic from get_weather.py)
# 4. Extract temperature and precipitation with error handling
# 5. Implement irrigation logic: recommend irrigation if precipitation < 5 mm and temperature > 25°C
# 6. Return a JSON response with latitude, longitude, temperature, precipitation, and advice
# Example: return jsonify({"latitude": lat, "advice": "Irrigation recommandée"})
@app.route('/conseil-irrigation')
def irrigation_advice():
    return jsonify({"message": "Not implemented yet"})

if __name__ == '__main__':
    app.run(debug=True)