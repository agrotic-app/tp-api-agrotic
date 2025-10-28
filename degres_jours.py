import requests
from datetime import date

def calculate_ddc(lat: float = 43.6119, lon: float = 3.8772):
    """
    Calcule les degrés-jours cumulés (DDC) entre le 1er mars et la date du jour,
    en utilisant les données historiques de l'API Open-Meteo.
    """

    # --- ⚙️ Configuration Agronomique ---
    # Température de base pour les graminées de foin (en °C)
    TEMPERATURE_BASE = 6  # °C
    # Seuil de DDC pour une maturité optimale (arbitraire pour l'exercice)
    SEUIL_DDC_MATURITE = 600  # °C.jours

    # --- 🧩 Exercice 1 : Construire la requête Open-Meteo Archive ---
    # TODO: Chercher l'URL de l'API Open-Meteo pour les données HISTORIQUES
    URL_HISTORIQUE = "..."  

    # TODO: Définir les dates de calcul
    # Le calcul commence le 1er mars de l'année en cours jusqu'à aujourd'hui
    START_DATE = 0
    END_DATE = 0

    params = {
        # TODO: Ajouter latitude, longitude, fuseau horaire
        # TODO: Ajouter les dates de début et de fin
        # TODO: Spécifier le paramètre 'daily' avec la clé de température moyenne
        "timezone": "Europe/Paris",
    }

    print(f"--- Calcul du DDC entre le {START_DATE} et le {END_DATE} ---")

    try:
        response = requests.get(URL_HISTORIQUE, params=params)
        response.raise_for_status()
        data = response.json()

        # --- 🧮 Exercice 2 : Calcul du DDC ---
        DDC_cumule = 0

        # TODO: Trouver la clé exacte des températures dans la réponse JSON
        temperatures = data.get('daily', {}).get('clé_à_trouver', [])

        if not temperatures:
            print("⚠️  Aucune donnée de température récupérée. Vérifiez vos paramètres.")
        else:
            for T_moyenne in temperatures:
                # TODO: Implémenter la formule du DDC : max(0, T_moyenne - T_base)
                degre_jour = ...
                DDC_cumule += degre_jour

            # --- Résultat intermédiaire ---
            print("\nRésultat du Calcul :")
            print(f"DDC cumulé ({START_DATE} → {END_DATE}) : {DDC_cumule:.2f} °C.jours")

            # --- Conseil agronomique ---
            if DDC_cumule > SEUIL_DDC_MATURITE:
                statut = "ATTEINTE"
                print(f"→ Maturité atteinte ({DDC_cumule:.2f} > {SEUIL_DDC_MATURITE})")
            else:
                statut = "PAS ENCORE ATTEINTE"
                print(f"→ Maturité non atteinte ({DDC_cumule:.2f} < {SEUIL_DDC_MATURITE})")

            # TODO: Retourner un dictionnaire avec les informations principales
            return {
                # "statut_maturite": ...,
                # "ddc_cumule": ...,
                # "seuil_maturite": ...,
            }

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la connexion à l'API Open-Meteo : {e}")
    except KeyError as e:
        print(f"Erreur de structure des données JSON. Clé manquante : {e}")
    except Exception as e:
        print(f"Une erreur inattendue est survenue : {e}")
