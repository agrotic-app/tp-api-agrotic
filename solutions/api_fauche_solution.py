"""
api_fauche_solution.py
Aggregates degres_jours, meteo_sechage and risque_faon to produce a final decision.
Rules:
- If DDC >= 600 and meteo_sechage == BON_SECHAGE and risque_faon_niveau < 8 -> FAUCHER
- Otherwise -> ATTENDRE (with reasons)
"""
from degres_jours_solution import calculate_ddc_solution
from meteo_sechage_solution import meteo_sechage_solution
from risque_faon_solution import calculer_risque_faon_solution

SEUIL_DDC = 600

def decision_fauche_solution(lat=43.6119, lon=3.8772, date_jour=None):
    ddc = calculate_ddc_solution(lat=lat, lon=lon, start_date=None, end_date=date_jour)
    meteo = meteo_sechage_solution(lat=lat, lon=lon, horizon_hours=48)
    risque = calculer_risque_faon_solution(date_str=date_jour, voisinage="champ_ouvert", annee_froide=False)

    reasons = []
    decision = "ATTENDRE"
    # Check DDC
    ddc_value = ddc.get("ddc_cumule") if isinstance(ddc, dict) else None
    if isinstance(ddc_value, (int, float)) and ddc_value >= SEUIL_DDC:
        reasons.append("DDC atteint")
    else:
        reasons.append("DDC non atteint")

    # Check meteo
    meteo_advice = meteo.get("conseil_sechage") if isinstance(meteo, dict) else None
    if meteo_advice == "BON_SECHAGE":
        reasons.append("Conditions de séchage favorables")
    else:
        reasons.append(f"Séchage défavorable ({meteo_advice})")

    # Check risque faon
    risque_val = risque.get("risque_faon_niveau") if isinstance(risque, dict) else None
    if isinstance(risque_val, (int, float)) and risque_val < 8.0:
        reasons.append("Risque faon acceptable")
    else:
        reasons.append("Risque faon élevé")

    if ("DDC atteint" in reasons) and ("Conditions de séchage favorables" in reasons) and ("Risque faon élevé" not in reasons):
        decision = "FAUCHER"

    justification = "; ".join(reasons)

    return {
        "decision_finale_fauche": decision,
        "justification": justification,
        "ddc": ddc,
        "meteo_sechage": meteo,
        "risque_faon": risque
    }
