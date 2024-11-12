# news.py

import os
import requests
from dotenv import load_dotenv
from datetime import datetime 

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")  # Schlüssel aus der Umgebungsvariablen
url = "https://newsapi.org/v2/everything"


def get_latest_news(topic=None, date=None):
    """Holt die neuesten Nachrichten basierend auf optionalen Filterparametern."""
    
    # Wenn kein Datum angegeben ist, heutiges Datum verwenden
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Parameter für die API-Anfrage
    params = {
        "from": date,             
        "sortBy": "popularity",
        "apiKey": API_KEY
    }

    # Nur hinzufügen, wenn ein Thema spezifiziert ist
    if topic:
        params["q"] = topic

    # Anfrage an die News API
    response = requests.get(url, params=params)
    
    # Prüfen, ob die Anfrage erfolgreich war
    if response.status_code == 200:
        return response.json()  # Gibt JSON als Dictionary zurück
    else:
        print("Fehler bei der Anfrage:", response.status_code)
        return {"articles": []}  # Leere Liste zurückgeben, wenn ein Fehler auftritt