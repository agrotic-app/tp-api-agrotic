# get_weather.py
import requests

# Coordonnées GPS de Montpellier
LATITUDE = 43.61
LONGITUDE = 3.87

# URL de base de l'API Open-Meteo
base_url = "https://api.open-meteo.com/v1/forecast"

# --- EXERCICE 1 : Construire la requête ---
#
# TODO: 1. Allez sur la documentation d'Open-Meteo : https://open-meteo.com/en/docs
# TODO: 2. Remplissez le dictionnaire 'params' ci-dessous pour demander :
#           - La météo actuelle ('current_weather')
#           - Le cumul de pluie journalier ('daily' -> 'precipitation_sum')
#           - Le fuseau horaire de Paris ('timezone')
#
params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    # ... Complétez ici avec les autres paramètres
}

print("Construction de la requête...")

# La librairie 'requests' va automatiquement construire l'URL finale à partir de la base et des paramètres
response = requests.get(base_url, params=params)

# --- La suite du code reste la même ---
# On vérifie si la requête a réussi (code de statut 200)
if response.status_code == 200:
    print("Succès ! Données reçues.")
    # On transforme la réponse (texte) en un dictionnaire Python (JSON)
    data = response.json()
    
    # Affichez l'URL que 'requests' a réellement appelée, pour vérification
    print(f"URL appelée : {response.url}")

    # --- EXERCICE 2 : Extraction ---
    #
    # TODO: 1. Naviguez dans le dictionnaire 'data' pour trouver la température actuelle.
    # TODO: 2. Stockez-la dans une variable nommée 'current_temp'.
    # TODO: 3. Affichez-la de manière propre avec un print().
    #
    # DÉFI: Faites de même pour le cumul de pluie prévu