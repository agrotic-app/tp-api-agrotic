# app.py
from flask import Flask, request, jsonify
import requests

# On crée l'application Flask
app = Flask(__name__)

# --- EXERCICE 3 : Route Principale ---
# Cette route est déjà fonctionnelle. Elle sert à vérifier que le serveur se lance bien.
@app.route('/')
def hello():
    return "Bienvenue sur l'Agro-Conseil API ! 🌾"


# --- EXERCICE 4 : Route pour le conseil d'irrigation ---
#
# TODO: Créez une nouvelle route '/conseil-irrigation' qui :
#   1. Récupère les paramètres d'URL 'lat' et 'lon'.
#   2. Appelle l'API Open-Meteo pour ces coordonnées (réutilisez le code de get_weather.py !).
#   3. Applique une logique simple : si le cumul de pluie est < 5mm, la décision est "OUI", sinon "NON".
#   4. Renvoie un objet JSON contenant les coordonnées, la pluie prévue et la décision.
#   5. (BONUS) Ajoute un "easter egg" pour une localisation amusante.
#
# @app.route('/conseil-irrigation')
# def irrigation_advice():
#     # ... Votre code ici ...
#     pass


# Cette partie permet de lancer le serveur en exécutant 'python app.py'
if __name__ == '__main__':
    app.run(debug=True)