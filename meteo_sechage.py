import requests

def get_meteo_sechage(lat: float = 43.6119, lon: float = 3.8772):
    """
    Analyse les prévisions météorologiques pour évaluer le risque de séchage du foin.
    Utilise l'API Open-Meteo pour obtenir les données horaires des 48 prochaines heures.
    """

    # --- ⚙️ Seuils agronomiques ---
    SEUIL_PLUIE_RISQUE = 0.1   # mm
    SEUIL_HUMIDITE_RISQUE = 70 # %
    SEUIL_HEURES_HUMIDES = 30  # heures sur 48 (si > 30, risque de séchage lent)

    # --- 🛰️ TODO 1 : Définir l'URL de l'API Open-Meteo pour les prévisions
    URL_PREVISIONS = ''

    # --- 🧾 TODO 2 : Compléter les paramètres de la requête ---
    params = {
        # TODO: ajouter latitude, longitude
        # TODO: préciser les variables horaires nécessaires (pluie et humidité)
        # TODO: limiter la prévision à 48h
        "timezone": "Europe/Paris",
    }

    print(f"--- Évaluation du Risque de Séchage pour les 48h à venir ---")

    try:
        response = requests.get(URL_PREVISIONS, params=params)
        response.raise_for_status()
        data = response.json()

          # TODO 3: Trouver la clé exacte des précipitations et de l'humidité dans la réponse JSON
        precipitations = data.get('hourly', {}).get('clé_pluie', [])
        humidites = data.get('hourly', {}).get('clé_humidité', [])

        risque_pluie_eleve = False
        compteur_heures_humides = 0
        conseil_final = "..." # TODO: à définir selon la logique

        if not precipitations or not humidites:
            print("⚠️ Données incomplètes. Vérifiez vos clés ou paramètres.")
        else:
            # --- 🔎 TODO 4 : Parcourir les 48 heures et appliquer les règles ---
            for i in range(len(precipitations)):
                # TODO: détecter les heures avec pluie
                # TODO: compter les heures avec humidité > seuil
                pass

            # --- 🧠 TODO 5 : Implémenter la logique de décision ---
            # if risque_pluie_eleve:
            #     conseil_final = "Risque de pluie détecté — reporter la fauche."
            # elif compteur_heures_humides > SEUIL_HEURES_HUMIDES:
            #     conseil_final = "Humidité élevée — séchage lent attendu."
            # else:
            #     conseil_final = "Conditions favorables au séchage."

            print("\nRésultats de l'analyse :")
            print(f"Heures > {SEUIL_HUMIDITE_RISQUE}% : {compteur_heures_humides}/48h")
            print(f"Pluie prévue : {'OUI' if risque_pluie_eleve else 'NON'}")
            print(f"-> CONSEIL : {conseil_final}")

        # --- ✅ TODO 6 : Retourner un résumé clair ---
        return {
            # TODO: retourner risque_sechage, conseil_sechage, résumé
        }

    except requests.exceptions.RequestException as e:
        print(f"\nErreur lors de la connexion à l'API Open-Meteo : {e}")
    except Exception as e:
        print(f"\nUne erreur inattendue est survenue : {e}")