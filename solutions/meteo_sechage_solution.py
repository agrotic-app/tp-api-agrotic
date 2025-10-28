"""
meteo_sechage_solution.py
Evaluates drying potential from Open-Meteo forecast API.
Endpoint: https://api.open-meteo.com/v1/forecast
We use hourly temperature, relative humidity and precipitation to assess drying.
"""
import requests
from datetime import datetime, timedelta

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def meteo_sechage_solution(lat=43.6119, lon=3.8772, horizon_hours=48):
    """
    Fetch forecast for next `horizon_hours` and compute a simple drying score.
    Returns a dict with computed metrics and a conseil_sechage string.
    """
    # request hourly variables
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,relativehumidity_2m,precipitation",
        "forecast_days": max(1, (horizon_hours // 24) + 1),
        "timezone": "Europe/Paris"
    }

    try:
        resp = requests.get(FORECAST_URL, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        return {"error": f"Open-Meteo forecast request failed: {e}", "params": params}

    hourly = data.get("hourly", {})
    temps = hourly.get("temperature_2m", [])
    rh = hourly.get("relativehumidity_2m", [])
    precip = hourly.get("precipitation", [])

    # limit to horizon_hours
    temps = temps[:horizon_hours]
    rh = rh[:horizon_hours]
    precip = precip[:horizon_hours]

    if not temps:
        return {"error": "No hourly temperature data from forecast", "params": params}

    humid_hours = sum(1 for v in rh if v is not None and float(v) >= 80.0)
    total_precip = sum(float(v) for v in precip if v is not None)

    # Simple heuristic:
    # - If precipitation expected in horizon -> ATTENDRE_POUR_SECHAGE
    # - Else if many humid hours (>30% of horizon) -> RISQUE_SECHAGE_LENT
    # - Else -> BON_SECHAGE
    if total_precip > 1e-6:
        conseil = "ATTENDRE_POUR_SECHAGE"
    elif humid_hours > 0.3 * horizon_hours:
        conseil = "RISQUE_SECHAGE_LENT"
    else:
        conseil = "BON_SECHAGE"

    return {
        "lat": lat,
        "lon": lon,
        "horizon_hours": horizon_hours,
        "humid_hours": humid_hours,
        "total_precip_mm": round(total_precip, 2),
        "conseil_sechage": conseil
    }
