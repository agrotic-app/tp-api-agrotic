import requests
from datetime import date

def calculate_ddc(lat: float = 43.6119,
                  lon: float = 3.8772):
    """Calculate cumulative degree-days (DDC) between two dates using Open-Meteo historical data.

    Parameters:
        lat: latitude in decimal degrees
        lon: longitude in decimal degrees

    Returns:
        A dict with keys: 'start_date', 'end_date', 'ddc', 'temperature_count', 'advice'
    """

    # --- ⚙️ Configuration Agronomique ---
    # Température de base pour les graminées de foin (en °C)
    TEMPERATURE_BASE = 6
    # Seuil de DDC pour une maturité optimale (arbitraire pour l'exercice)
    SEUIL_DDC_MATURITE = 600

    # TODO: Chercher l'URL de l'API Open-Meteo pour les données HISTORIQUES
    URL_HISTORIQUE = "..." 

    # # TODO: Période de calcul : du 1er Mars de l'année en cours jusqu'à aujourd'hui
    START_DATE = 0
    END_DATE = 0

    # --- 🛠️ Exercice 1 : Construire la Requête ---
    params = {
        # TODO: Ajouter les paramètres pour la latitude, la longitude, le fuseau horaire
        # TODO: Ajouter les dates de début et de fin 
        # TODO: Spécifier le paramètre 'daily' avec la bonne clé pour la température moyenne
        "latitude": lat,
        "longitude": lon,
        "timezone": "Europe/Paris", 
        "start_date": START_DATE,
        "end_date": END_DATE,
        # "daily": ["clé_à_trouver"], 
    }

    print(f"--- Calcul du DDC entre le {START_DATE} et le {END_DATE} ---")

    try:
        response = requests.get(URL_HISTORIQUE, params=params)
        response.raise_for_status() # Lève une exception si le statut HTTP est 4xx ou 5xx
        data = response.json()

        # --- 🛠️ Exercice 2 : Calculer le DDC ---
        DDC_cumule = 0

        # TODO: Trouver la clé exacte des températures dans la réponse JSON (data)
        # La structure est typiquement data['daily']['clé_exacte']
        temperatures = data.get('daily', {}).get('clé_à_trouver', [])

        if not temperatures:
            print("Erreur : Aucune donnée de température récupérée. Vérifiez votre URL ou vos paramètres.")
        else:
            for T_moyenne in temperatures:
                # TODO: Implémenter la formule du DDC : max(0, T_moyenne - T_base)
                degre_jour = ... 
                DDC_cumule += degre_jour

            # --- Affichage du résultat ---
            print("\nRésultat du Calcul :")
            print(f"DDC cumulé ({START_DATE} -> {END_DATE}) : {DDC_cumule:.2f} °C.jours")

            # --- Conseil Agronomique ---
            if DDC_cumule > SEUIL_DDC_MATURITE:
                print(f"-> CONSEIL MATURITÉ : ATTEINTE ({DDC_cumule:.2f} > {SEUIL_DDC_MATURITE}).")
            else:
                print(f"-> CONSEIL MATURITÉ : PAS ENCORE ATTEINTE ({DDC_cumule:.2f} < {SEUIL_DDC_MATURITE}).")


    except requests.exceptions.RequestException as e:
        print(f"\nErreur lors de la connexion à l'API Open-Meteo : {e}")
    except KeyError as e:
        print(f"\nErreur de structure des données JSON. Clé manquante : {e}. Assurez-vous que les paramètres sont corrects.")
    except Exception as e:
        print(f"\nUne erreur inattendue est survenue : {e}")