from datetime import date, timedelta

# --- ⚙️ Configuration du Modèle ---
PERIODE_RISQUE_BASE = {
    "debut_moyen": date.fromisoformat('2026-05-15'),
    "debut_eleve": date.fromisoformat('2026-06-01'),
    "fin_eleve": date.fromisoformat('2026-06-20'),
    "fin_moyen": date.fromisoformat('2026-06-30'),
}

MULTI_VOISINAGE = {
    "foret": 1.5,
    "haie_bocagere": 1.3,
    "champ_ouvert": 1.0,
    "defaut": 1.0
}

def calculer_risque_faon(date_fauche_str: str, type_voisinage: str, annee_froide: bool) -> dict:
    """
    Calcule un score de risque faunistique (faons) sur une échelle de 1 à 10.

    Arguments:
        date_fauche_str (str): Date prévue de la fauche (AAAA-MM-JJ)
        type_voisinage (str): foret / haie_bocagere / champ_ouvert
        annee_froide (bool): True si l’année précédente était froide (retarde la période)
    """
    try:
        date_fauche = date.fromisoformat(date_fauche_str)
    except ValueError:
        return {"erreur": "Format de date incorrect. Utilisez AAAA-MM-JJ."}

    # --- 🧩 TODO 1 : Décalage saisonnier ---
    # Si annee_froide est True, décaler toutes les bornes de PERIODE_RISQUE_BASE de +7 jours
    # Astuce : utilisez timedelta(days=7)
    bornes_ajustees = PERIODE_RISQUE_BASE.copy()
    # Exemple attendu :
    # if annee_froide:
    #     bornes_ajustees = {k: v + timedelta(days=7) for k, v in PERIODE_RISQUE_BASE.items()}

    # --- 🧮 TODO 2 : Déterminer le score de base selon la date ---
    # Utilisez les bornes ajustées pour identifier le niveau de risque :
    # - Si date_fauche < debut_moyen ou > fin_moyen → score_base = 2
    # - Si date entre debut_moyen et debut_eleve OU entre fin_eleve et fin_moyen → score_base = 5
    # - Si date entre debut_eleve et fin_eleve → score_base = 8
    score_base = 2

    # --- 🧱 TODO 3 : Appliquer le multiplicateur de voisinage ---
    # Récupérer la valeur dans MULTI_VOISINAGE selon type_voisinage
    multiplicateur = MULTI_VOISINAGE.get(type_voisinage, MULTI_VOISINAGE["defaut"])

    # --- ⚗️ TODO 4 : Calculer le score final ---
    # score_final = score_base * multiplicateur
    # Limiter à un maximum de 10.0 et arrondir à 2 décimales
    score_final = 0.0

    # --- 💬 TODO 5 : Générer le conseil selon le score ---
    # if score_final >= 7.0:
    #     conseil = "Fauche à haut risque - Utiliser un système d'effarouchement ou de balayage."
    # elif score_final >= 4.0:
    #     conseil = "Fauche à risque modéré - Procéder avec vigilance."
    # else:
    #     conseil = "Fauche à risque faible - Procéder normalement."
    conseil = "..."

    # --- 🧾 Justification ---
    justification = f"Score de base ({score_base}) ajusté par le voisinage ({multiplicateur}x). Décalage saisonnier : {'OUI' if annee_froide else 'NON'}."

    # --- ✅ TODO 6 : Retourner la réponse ---
    return {
    }

# --- 🧪 Exemple de Test ---
if __name__ == '__main__':
    print("--- Test 1 : Plein Risque ---")
    print(calculer_risque_faon("2026-06-10", "foret", False))

    print("\n--- Test 2 : Risque Modéré Décalé ---")
    print(calculer_risque_faon("2026-05-20", "champ_ouvert", True))
