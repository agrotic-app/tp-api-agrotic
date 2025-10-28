from flask import Flask, request, jsonify
# Importe le module CORS pour l'accès depuis le fichier HTML (client)
try:
    from flask_cors import CORS
except ImportError:
    # Fonction de substitution si Flask-CORS n'est pas installé
    def CORS(app): return app 

# Importe toutes les fonctions et constantes nécessaires depuis le module de logique
from api_fauche import (
    get_soil_texture, 
    fetch_all_data, 
    decision_finale_fauche, 
    LATITUDE, 
    LONGITUDE, 
    DATE_JOUR
)

from degres_jours import calculate_ddc 
from meteo_sechage import get_meteo_sechage
from risque_faon import calculer_risque_faon

app = Flask(__name__)
CORS(app) # Activation de CORS pour toutes les routes

# --- ROUTES PRINCIPALES (API MÈRE) ---

@app.route('/')
def home():
    # Route de base pour le test simple
    return "Bienvenue sur l'API de Décision de Fauche. Utilisez le point d'accès '/api-decision-fauche' pour la requête finale."

# Route principale appelée par le client (HTML)
@app.route('/api-decision-fauche')
def decision_fauche():
    
    # 1. Récupérer l'information externe (Sol)
    type_sol = get_soil_texture(LATITUDE, LONGITUDE)
    
    # 2. Récupérer les données des APIs Filles (Mock ou Réel)
    ddc, meteo, faon = fetch_all_data(LATITUDE, LONGITUDE, DATE_JOUR)
    
    # 3. Prendre la Décision (Fonction pure sans dépendance HTTP)
    resultat_final = decision_finale_fauche(ddc, meteo, faon, type_sol)
    
    # 4. Renvoyer la réponse HTTP
    return jsonify(resultat_final)


@app.route("/api-degres-jours", methods=["GET"])
def api_degres_jours():
    lat = float(request.args.get("lat", LATITUDE))
    lon = float(request.args.get("lon", LONGITUDE))
    result = calculate_ddc(lat=lat, lon=lon)
    return jsonify(result)

@app.route("/api-meteo-sechage", methods=["GET"])
def api_meteo_sechage():
    lat = float(request.args.get("lat", LATITUDE))
    lon = float(request.args.get("lon", LONGITUDE))
    result = get_meteo_sechage(lat=lat, lon=lon)
    return jsonify(result)

@app.route("/api-risque-faon", methods=["GET"])
def api_risque_faon():
    date_str = request.args.get("date")
    voisinage = request.args.get("voisinage", "defaut")
    annee_froide = request.args.get("annee_froide", "false").lower() in ("1","true","yes")
    result = calculer_risque_faon(date_str=date_str, voisinage=voisinage, annee_froide=annee_froide)
    return jsonify(result)


if __name__ == '__main__':
    # Utilisation du port 5000 pour l'API Mère
    app.run(debug=True, port=5000)