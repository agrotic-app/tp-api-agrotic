import requests

def get_meteo_sechage(lat: float = 43.6119,
                  lon: float = 3.8772):
    """
    Analyse les prévisions météorologiques pour évaluer le risque de séchage du foin.
    Utilise l'API Open-Meteo pour obtenir les données horaires des 48 prochaines heures.
    """

    # --- ⚙️ Configuration Agronomique ---
    SEUIL_PLUIE_RISQUE = 0.1 # mm
    SEUIL_HUMIDITE_RISQUE = 70 # %
    SEUIL_HEURES_HUMIDES = 30 # heures sur 48 (si > 30, risque de séchage lent)

    # TODO: Chercher l'URL de l'API Open-Meteo pour les PRÉVISIONS
    URL_PREVISIONS = "..." 

    # --- 🛠️ Exercice 3 : Construire la Requête ---
    params = {
        # TODO: Ajouter les paramètres pour la latitude, la longitude, le fuseau horaire
        # TODO: Spécifier le paramètre 'hourly' pour les précipitations et l'humidité
        # TODO: Limiter la prévision aux 48 prochaines heures (2 jours)
        "latitude": lat,
        "longitude": lon,
        "timezone": "Europe/Paris",
        "forecast_days": 2, 
        # "hourly": ["clé_pluie", "clé_humidité"], 
    }

    print(f"--- Évaluation du Risque de Séchage pour les 48h à venir ---")

    try:
        response = requests.get(URL_PREVISIONS, params=params)
        response.raise_for_status()
        data = response.json()

        # --- 🛠️ Exercice 4 : Calculer le Risque ---
        
        # TODO: Trouver la clé exacte des précipitations et de l'humidité dans la réponse JSON
        precipitations = data.get('hourly', {}).get('clé_pluie', [])
        humidites = data.get('hourly', {}).get('clé_humidité', [])

        risque_pluie_eleve = False
        compteur_heures_humides = 0
        conseil_final = "..." # Initialiser le conseil

        if not precipitations or not humidites:
            print("Erreur : Données incomplètes. Vérifiez les clés de votre requête.")
        else:
            # 1. Parcourir les données pour collecter les risques
            for i in range(len(precipitations)):
                # Risque de Pluie
                if precipitations[i] > SEUIL_PLUIE_RISQUE:
                    risque_pluie_eleve = True
                
                # Risque de Séchage Lent
                if humidites[i] > SEUIL_HUMIDITE_RISQUE:
                    compteur_heures_humides += 1

            # 2. TODO: Implémenter la Logique de Décision Agronomique (if/elif/else)
            # La hiérarchie est: Pluie > Séchage Lent > Recommandé
            
            # Exemple de structure:
            # if risque_pluie_eleve:
            #     conseil_final = "..."
            # elif compteur_heures_humides > SEUIL_HEURES_HUMIDES:
            #     conseil_final = "..."
            # else:
            #     conseil_final = "..."

            # --- Affichage et Conclusion ---
            print("\nRésultats de l'analyse :")
            print(f"Heures de forte humidité (> {SEUIL_HUMIDITE_RISQUE}%) : {compteur_heures_humides}/48h")
            print(f"Prévision de pluie > {SEUIL_PLUIE_RISQUE}mm : {'OUI' if risque_pluie_eleve else 'NON'}")
            
            print(f"-> CONSEIL SÉCHAGE : {conseil_final}")


    except requests.exceptions.RequestException as e:
        print(f"\nErreur lors de la connexion à l'API Open-Meteo : {e}")
    except Exception as e:
        print(f"\nUne erreur inattendue est survenue : {e}")