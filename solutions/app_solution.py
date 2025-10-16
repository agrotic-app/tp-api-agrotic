from flask import Flask, jsonify, request
from api_fauche_solution import decision_fauche_solution
from degres_jours_solution import calculate_ddc_solution
from meteo_sechage_solution import meteo_sechage_solution
from risque_faon_solution import calculer_risque_faon_solution

app = Flask(__name__)

@app.route("/api-decision-fauche", methods=["GET"])
def api_decision_fauche():
    lat = float(request.args.get("lat", 43.6119))
    lon = float(request.args.get("lon", 3.8772))
    date_jour = request.args.get("date")  # ISO format or None
    result = decision_fauche_solution(lat=lat, lon=lon, date_jour=date_jour)
    return jsonify(result)

@app.route("/api-degres-jours", methods=["GET"])
@app.route("/api-degres-jour", methods=["GET"])
def api_degres_jours():
    lat = float(request.args.get("lat", 43.6119))
    lon = float(request.args.get("lon", 3.8772))
    start = request.args.get("start")  # ISO date or None
    end = request.args.get("end")      # ISO date or None
    result = calculate_ddc_solution(lat=lat, lon=lon, start_date=start, end_date=end)
    return jsonify(result)

@app.route("/api-meteo-sechage", methods=["GET"])
@app.route("/api-meteo", methods=["GET"])
def api_meteo_sechage():
    lat = float(request.args.get("lat", 43.6119))
    lon = float(request.args.get("lon", 3.8772))
    horizon = int(request.args.get("horizon", 48))
    result = meteo_sechage_solution(lat=lat, lon=lon, horizon_hours=horizon)
    return jsonify(result)

@app.route("/api-risque-faon", methods=["GET"])
@app.route("/api-risque-faoen", methods=["GET"])
def api_risque_faon():
    date_str = request.args.get("date")
    voisinage = request.args.get("voisinage", "champ_ouvert")
    annee_froide = request.args.get("annee_froide", "false").lower() in ("1","true","yes")
    result = calculer_risque_faon_solution(date_str=date_str, voisinage=voisinage, annee_froide=annee_froide)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
