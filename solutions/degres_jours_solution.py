"""
degres_jours_solution.py
Calcul du DDC (Degrés-Jours de Croissance) en utilisant l'API historique d'Open-Meteo.
Endpoint utilisé: https://archive-api.open-meteo.com/v1/archive

Function: calculate_ddc_solution(lat, lon, start_date, end_date)
Returns: dict with cumulative DDC and metadata.
"""
import requests
from datetime import date, datetime

TEMPERATURE_BASE = 6
SEUIL_DDC_MATURITE = 600

ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

def _parse_date(d):
    if d is None:
        return None
    if isinstance(d, date):
        return d
    return datetime.fromisoformat(d).date()

def calculate_ddc_solution(lat=43.6119, lon=3.8772, start_date=None, end_date=None):
    """
    Calculate cumulative degree-days from start_date to end_date using Open-Meteo archive API.
    If start_date is None, use March 1st of the current year.
    If end_date is None, use today.
    """
    if end_date is None:
        end = date.today()
    else:
        end = _parse_date(end_date)

    if start_date is None:
        start = date(date.today().year, 3, 1)
    else:
        start = _parse_date(start_date)

    if start > end:
        start, end = end, start

    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "daily": "temperature_2m_mean",
        "timezone": "Europe/Paris"
    }

    try:
        resp = requests.get(ARCHIVE_URL, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"error": f"Open-Meteo archive request failed: {e}", "params": params}

    temps = data.get("daily", {}).get("temperature_2m_mean", [])
    if not temps:
        return {"error": "No temperature data returned from Open-Meteo", "params": params, "data_sample": data.get("daily", {})}

    ddc_cumule = 0.0
    for T in temps:
        try:
            degre_jour = max(0.0, float(T) - TEMPERATURE_BASE)
        except Exception:
            degre_jour = 0.0
        ddc_cumule += degre_jour

    conseil = "ATTEINTE" if ddc_cumule >= SEUIL_DDC_MATURITE else "PAS_ENCORE_ATTEINTE"

    return {
        "lat": lat,
        "lon": lon,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "jours": (end - start).days + 1,
        "ddc_cumule": round(ddc_cumule, 2),
        "seuil_ddc_maturite": SEUIL_DDC_MATURITE,
        "conseil_maturite": conseil
    }
