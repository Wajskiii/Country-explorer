from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/countries")
def get_countries():
    try:
        r = requests.get("https://restcountries.com/v3.1/all?fields=name", timeout=10)
        data = r.json()
        
        countries = []
        for c in data:
            name = c.get("name", {}).get("common", "")
            if name:
                countries.append({"name": name})
        
        countries.sort(key=lambda x: x["name"])
        
        print(f"Vraćam {len(countries)} država")
        return jsonify(countries)
    
    except Exception as e:
        print(f"Greška: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return jsonify({"message": "hallloo"})

@app.route("/country")
def get_country():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "Nedostaje naziv"}), 400
    
    try:
        url = f"https://restcountries.com/v3.1/name/{name}"
        r = requests.get(url, timeout=10)
        
        if r.status_code != 200:
            return jsonify({"error": "Država nije pronađena"}), 404
        
        data = r.json()[0]
        
        # Valuta
        currency = {}
        if "currencies" in data:
            code = list(data["currencies"].keys())[0]
            currency = {code: data["currencies"][code]}
        
        # Jezici
        languages = data.get("languages", {})
        
        result = {
            "name": data.get("name", {}).get("common"),
            "flag": data.get("flags", {}).get("svg"),
            "capital": data.get("capital", ["N/A"])[0],
            "continent": data.get("continents", ["N/A"])[0],
            "population": data.get("population"),
            "area": data.get("area"),
            "currencies": currency,
            "timezones": data.get("timezones", []),
            "languages": languages,
            "borders": data.get("borders", []),
            "maps": data.get("maps", {}).get("googleMaps")
        }
        return jsonify(result)
    
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)