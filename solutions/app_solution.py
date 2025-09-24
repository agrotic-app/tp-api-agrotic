from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

# Crop water requirements (mm/day)
CROP_WATER_NEEDS = {
    "mais": 5,
    "vigne": 3,
    "ble": 4
}

@app.route('/')
def home():
    return "Bienvenue sur l'API AgroTIC !"

@app.route('/conseil-irrigation')
def irrigation_advice():
    # Get parameters from query
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    crop_type = request.args.get('type_culture', 'mais')
    
    # Validate parameters
    if not lat or not lon:
        abort(400, description="Paramètres latitude ou longitude manquants")
    
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        abort(400, description="Latitude et longitude doivent être des nombres valides")
    
    if crop_type not in CROP_WATER_NEEDS:
        abort(400, description=f"Type de culture invalide. Choisissez parmi {list(CROP_WATER_NEEDS.keys())}")
    
    # Call Open-Meteo API
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true",
        "daily": ["precipitation_sum", "et0_fao_evapotranspiration"],
        "timezone": "Europe/Paris"
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        abort(500, description="Échec de la récupération des données météo")
    
    data = response.json()
    temperature = data.get('current_weather', {}).get('temperature', 'N/A')
    precipitation = data.get('daily', {}).get('precipitation_sum', [0])[0]
    evapotranspiration = data.get('daily', {}).get('et0_fao_evapotranspiration', [0])[0]
    
    # Irrigation logic
    water_need = CROP_WATER_NEEDS[crop_type]
    advice = "Irrigation recommandée" if evapotranspiration > 4 and precipitation < water_need else "Pas d'irrigation nécessaire"
    
    return jsonify({
        "latitude": lat,
        "longitude": lon,
        "crop_type": crop_type,
        "temperature": temperature,
        "precipitation": precipitation,
        "evapotranspiration": evapotranspiration,
        "advice": advice
    })

@app.route('/precipitation-data')
def precipitation_data():
    # Get latitude and longitude from query parameters
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    if not lat or not lon:
        abort(400, description="Paramètres latitude ou longitude manquants")
    
    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        abort(400, description="Latitude et longitude doivent être des nombres valides")
    
    # Call Open-Meteo API for 5 days of precipitation
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_sum",
        "timezone": "Europe/Paris",
        "forecast_days": 5
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        abort(500, description="Échec de la récupération des données météo")
    
    data = response.json()
    precipitation = data.get('daily', {}).get('precipitation_sum', [0] * 5)
    
    return jsonify({
        "labels": [f"Jour {i+1}" for i in range(5)],
        "precipitation": precipitation
    })

if __name__ == '__main__':
    app.run(debug=True)