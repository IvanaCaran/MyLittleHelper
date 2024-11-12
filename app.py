from flask import Flask, render_template, request, jsonify
from weather import get_lat_lon, get_current_weather
from news import get_latest_news
from dotenv import load_dotenv
import os


load_dotenv()

api_key = os.getenv("WEATHER_API_KEY")
api_key = os.getenv("API_KEY")

app = Flask(__name__)

#Startseite
@app.route("/")
def startseite():
    return render_template("Startseite.html")

#Wecker
@app.route("/wecker")
def wecker():
    return render_template("wecker.html")

# News
@app.route('/news', methods=["GET", "POST"])
def news_page():
   
    topic = None
    date = None

    if request.method == "POST":
        topic = request.form.get('topic')
        date = request.form.get('date')

    # Abruf der Nachrichten basierend auf Thema und Datum oder ohne Filter
    news_data = get_latest_news(topic, date)

    # Die Nachrichten an die Vorlage `news.html` übergeben
    return render_template("news.html", news_data=news_data)

#Wetterbericht

@app.route("/wetter", methods=["GET", "POST"])
def index():
    weather_data = None

    if request.method == "POST":
        # Daten aus dem Formular abrufen
        city_name = request.form.get("cityName")
        state_name = request.form.get("stateName", "")
        country_name = request.form.get("countryName", "DE")

        # Koordinaten abrufen
        lat, lon = get_lat_lon(city_name, state_name, country_name, api_key)
        if lat is not None and lon is not None:
            # Wetterdaten abrufen
            weather_data = get_current_weather(lat, lon, api_key)
        else:
            print("Standort konnte nicht gefunden werden.")

    return render_template("wetter.html", data=weather_data)

# Flask-Anwendung ausführen
if __name__ == "__main__":
    app.run(debug=True)
