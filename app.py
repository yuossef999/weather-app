from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city", "").strip()
    if not city:
        return render_template("error.html", message="City is required")

    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1, "language": "en", "format": "json"},
        timeout=10
    ).json()

    if "results" not in geo or not geo["results"]:
        return render_template("error.html", message="City not found")

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]

    w = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon, "current_weather": True},
        timeout=10
    ).json()

    current = w.get("current_weather", {})
    return render_template("weather.html", city=city, current=current)

if __name__ == "__main__":
    app.run(debug=True)
