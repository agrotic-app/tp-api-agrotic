from datetime import date


# --- ⚙️ Configuration du Modèle ---
# Définition des bornes de risque (par défaut, pour une année "normale")
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
        date_fauche_str (str): Date prévue de la fauche au format ISO (AAAA-MM-JJ).
        type_voisinage (str): Type d'environnement à proximité (foret, haie_bocagere, champ_ouvert).
        annee_froide (bool): Indique si l'hiver précédent était rigoureux.

    Retourne:
        dict: Le score de risque et le conseil.
    """
    try:
        date_fauche = date.fromisoformat(date_fauche_str)
    except ValueError:
        return {"erreur": "Format de date incorrect. Utilisez AAAA-MM-JJ."}

    # 1. TODO: Implémenter le Décalage Saisonnier
    # Si annee_froide est True, décaler toutes les dates de la PERIODE_RISQUE_BASE de 7 jours.
    # Utilisez timedelta(days=7)

    bornes_ajustees = PERIODE_RISQUE_BASE.copy()
    if annee_froide:
        print("Logique : Décalage de la période de mise bas de 7 jours (année froide)")
        # Exemple de décalage: bornes_ajustees["debut_moyen"] += timedelta(days=7)
        # TODO: Appliquer le décalage aux quatre bornes.
        
    
    # 2. TODO: Calculer le Score de Base
    score_base = 2 # Risque Faible par défaut
    
    # La hiérarchie est: Élevé > Moyen > Faible
    if bornes_ajustees["debut_eleve"] <= date_fauche <= bornes_ajustees["fin_eleve"]:
        score_base = 8 # Pleine période de risque
    elif bornes_ajustees["debut_moyen"] <= date_fauche <= bornes_ajustees["fin_moyen"]:
        score_base = 5 # Période moyenne
    
    
    # 3. TODO: Appliquer le Multiplicateur de Voisinage
    multiplicateur = MULTI_VOISINAGE.get(type_voisinage, MULTI_VOISINAGE["defaut"])
    score_final = score_base * multiplicateur
    
    # 4. Normalisation et Conclusion
    score_final = round(min(score_final, 10.0), 2)
    
    if score_final >= 7.0:
        conseil = "Fauche à haut risque - Utiliser un système d'effarouchement ou de balayage."
    elif score_final >= 4.0:
        conseil = "Fauche à risque modéré - Procéder avec vigilance."
    else:
        conseil = "Fauche à risque faible - Procéder normalement."
    
    justification = f"Score de base ({score_base}) ajusté par le voisinage ({multiplicateur}x). Décalage saisonnier : {'OUI' if annee_froide else 'NON'}."

    return {
        "risque_faon_niveau": score_final,
        "conseil_faune": conseil,
        "justification": justification
    }

# --- Exemple de Test (À laisser pour validation) ---
if __name__ == '__main__':
    # Test 1: Pleine période, Voisinage Forêt, Année Normale
    print("--- Test 1 : Plein Risque ---")
    resultat = calculer_risque_faon("2026-06-10", "foret", False)
    # Attendu: Score de base 8 * 1.5 = 12 -> 10.0
    print(resultat)
    
    # Test 2: Période Moyenne, Champ Ouvert, Année Froide (décalé)
    print("\n--- Test 2 : Risque Modéré Décalé ---")
    resultat = calculer_risque_faon("2026-05-20", "champ_ouvert", True)
    # Attendu: La date 20/05 tombe dans la période Moyenne (5) * 1.0
    print(resultat)