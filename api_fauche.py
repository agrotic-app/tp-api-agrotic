import requests
import json
from datetime import date

# --- 🌍 Configuration Globale ---
LATITUDE = 43.6119
LONGITUDE = 3.8772
DATE_JOUR = date.today().isoformat()

# URLs MOCK (à décommenter pour les appels réels)
# TODO: Remplacer l'IP par les adresses réelles des binômes !
URL_DDC = "http://192.168.1.XX:5000/api-degres-jours"
URL_METEO = "http://192.168.1.XX:5000/api-meteo-sechage"
URL_FAON = "http://192.168.1.XX:5000/api-risque-faon"
# TODO: Chercher l'URL de l'API ISRIC (Sol)
URL_ISRIC = "..."

# --- MOCK DES DONNÉES FILLES (Utiliser ceci pour commencer) ---
MOCK_DATA = {
    "DDC": {"statut_maturite": "ATTEINTE", "ddc_cumule": 655.2, "seuil_maturite": 600},
    "METEO": {"conseil_sechage": "Fauchage Recommandé"},
    "FAON": {"risque_faon_niveau": 3.2},
}


# --- 🛠️ Exercice 6.1 : API Externe Sol ---
def get_soil_texture(lat, lon):
    """
    Appelle l'API ISRIC pour obtenir le type de sol.
    Le but est de valider la connexion à l'API externe (URL et Params).
    """

    # TODO: Définir les paramètres pour la lat, lon, la propriété (ex: 'clay') et la profondeur ('0-5cm')
    params = {
        "lat": lat,
        "lon": lon,
        # ... à compléter ...
    }

    print("STATUS: Tentative d'appel à l'API ISRIC (Sol)...")
    try:
        # TODO: Décommenter l'appel réel après avoir complété les params
        # response = requests.get(URL_ISRIC, params=params, timeout=5)
        # response.raise_for_status()

        # Simuler le résultat après avoir validé l'appel.
        print("STATUS: Connexion ISRIC réussie. Utilisation du Mock.")
        if lat > 43.6:
            return "Limon Argileux (Mock)"
        else:
            return "Sable Limoneux (Mock)"

    except requests.exceptions.RequestException as e:
        print(f"Erreur API ISRIC: {e}. Le sol est Inconnu.")
        return "Inconnu (Erreur API)"
    except Exception as e:
        print(f"Erreur lors de l'extraction des données ISRIC: {e}")
        return "Inconnu (Erreur interne)"


def fetch_all_data(lat, lon, date_str):
    """
    Simule ou appelle réellement toutes les APIs filles.
    """

    # 1. Utilisation des MOCK_DATA (Par défaut)
    print("\nSTATUS: Utilisation des données MOCK des APIs filles.")
    ddc_data = MOCK_DATA["DDC"]
    meteo_data = MOCK_DATA["METEO"]
    faon_data = MOCK_DATA["FAON"]

    # 2. TODO: APPEL RÉEL (Décommenter quand les binômes sont prêts)
    """
    print("\nSTATUS: Tentative d'appel aux APIs filles réelles...")
    try:
        # NOTE: Les APIs filles doivent être prêtes (Flask lancé) sur l'IP spécifiée
        ddc_data = requests.get(URL_DDC, params={"lat": lat, "lon": lon}, timeout=5).json()
        meteo_data = requests.get(URL_METEO, timeout=5).json()
        faon_data = requests.get(URL_FAON, params={"date": date_str, "lat": lat, "lon": lon}, timeout=5).json()
        print("STATUS: Appels API réels réussis.")
    except Exception as e:
        print(f"Erreur lors de l'appel d'une API fille : {e}. Fallback aux MOCK_DATA.")
        ddc_data = MOCK_DATA["DDC"]
        meteo_data = MOCK_DATA["METEO"]
        faon_data = MOCK_DATA["FAON"]
    """

    return ddc_data, meteo_data, faon_data


# --- ⚙️ Exercice 6.2 : Fonction Principale de Décision ---
def decision_finale_fauche(ddc_data, meteo_data, faon_data, type_sol):
    """
    Applique la logique de veto et prend la décision finale.
    """

    # Récupération des indicateurs clés
    statut_maturite = ddc_data.get("statut_maturite", "INCONNU")
    conseil_sechage = meteo_data.get("conseil_sechage", "INCONNU")
    risque_faon = faon_data.get("risque_faon_niveau")

    decision = "OUI"
    justification = "Conditions Optimales"

    # 1. TODO: Implémenter la LOGIQUE DE VETO (if/elif/else)
    # Appliquer les règles de décision finale du README :
    # - Veto Météo
    # - Veto Maturité
    # - Veto Faune
    #
    # Exemple de structure :
    # if conseil_sechage != "Fauchage Recommandé":
    #     decision = "NON"
    #     justification = f"Risque Météo: {conseil_sechage}"
    # elif statut_maturite != "ATTEINTE":
    #     ...
    # elif risque_faon > 7.0:
    #     ...
    # else:
    #     decision = "OUI"
    #     justification = "Conditions Optimales"

    # Note: On enrichit toujours la justification avec la donnée Sol
    justification_finale = f"{justification}. (Sol: {type_sol})"

    return {
        "decision_finale_fauche": decision,
        "justification": justification_finale,
        "facteurs_cles": {
            "maturite_ddc": ddc_data.get("ddc_cumule"),
            "conseil_sechage": conseil_sechage,
            "risque_faon_niveau": risque_faon,
            "type_sol": type_sol,
        },
    }
