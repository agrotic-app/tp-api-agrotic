"""
risque_faon_solution.py
Implements the "Risque Faons" model described in the README.

Rules implemented:
- Periods:
  * Low (score base 2): outside critical period
  * Medium (score base 5): beginning or end of period (15-31 May, 21-30 June)
  * High (score base 8): peak period (1-20 June)
- If annee_froide=True, shift all boundaries by +7 days
- voisinage multiplier: forest/haies -> x1.5, champ_ouvert -> x1.0
- Final score capped to 10, returned with textual advice and justification
"""
from datetime import date, datetime, timedelta

def _parse_date(d):
    if d is None:
        return date.today()
    if isinstance(d, date):
        return d
    return datetime.fromisoformat(d).date()

def calculer_risque_faon_solution(date_str=None, voisinage="champ_ouvert", annee_froide=False):
    d = _parse_date(date_str)

    shift = timedelta(days=7) if annee_froide else timedelta(days=0)

    # Define base intervals (month-day tuples)
    year = d.year
    # Note: intervals include both bounds
    periode_moyen_1_start = date(year, 5, 15) + shift
    periode_moyen_1_end   = date(year, 5, 31) + shift
    periode_haut_start    = date(year, 6, 1)  + shift
    periode_haut_end      = date(year, 6, 20) + shift
    periode_moyen_2_start = date(year, 6, 21) + shift
    periode_moyen_2_end   = date(year, 6, 30) + shift

    base_score = 2
    justification_period = "Hors période critique"
    if periode_haut_start <= d <= periode_haut_end:
        base_score = 8
        justification_period = "Pleine période de mise bas"
    elif periode_moyen_1_start <= d <= periode_moyen_1_end:
        base_score = 5
        justification_period = "Début de période (15-31 mai)"
    elif periode_moyen_2_start <= d <= periode_moyen_2_end:
        base_score = 5
        justification_period = "Fin de période (21-30 juin)"

    voisinage = (voisinage or "champ_ouvert").lower()
    if voisinage in ("foret", "haies", "parcelle_bordee_de_foret", "parcelle_bordee_de_haies"):
        mult = 1.5
        voisinage_label = "Parcelle bordée de Forêt / Haies"
    else:
        mult = 1.0
        voisinage_label = "Champ ouvert"

    score = base_score * mult
    score = min(10.0, round(score, 2))

    if score >= 8.0:
        conseil = "Fauche à haut risque - Utiliser un système d'effarouchement"
    elif score >= 4.0:
        conseil = "Risque modéré - vigilance"
    else:
        conseil = "Faible risque pour la faune"

    justification = f"{justification_period} (base {base_score}) multiplié par la proximité ({voisinage_label}, x{mult})."

    return {
        "risque_faon_niveau": score,
        "conseil_faune": conseil,
        "justification": justification,
        "date": d.isoformat(),
        "voisinage": voisinage
    }
