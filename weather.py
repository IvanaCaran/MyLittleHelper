import requests
from dataclasses import dataclass

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: float

def get_lat_lon(city_name, state_code, country_code, API_key):
    """Liefert die Breitengrad- und Längengradkoordinaten einer Stadt."""
    try:
        response = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_key}"
        )
        response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
        data = response.json()
        if data:
            lat, lon = data[0].get("lat"), data[0].get("lon")
            return lat, lon
        else:
            print("Ort nicht gefunden.")
            return None, None
    except requests.exceptions.RequestException as e:
        print("Fehler bei der Anfrage:", e)
        return None, None

def get_current_weather(lat, lon, API_key):
    """Liefert aktuelle Wetterdaten für die angegebenen Koordinaten."""
    try:
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_key}&units=metric"
        )
        response.raise_for_status()  # Überprüfen, ob die Anfrage erfolgreich war
        data = response.json()
        return WeatherData(
            main=data.get("weather", [{}])[0].get("main", "Keine Daten"),
            description=data.get("weather", [{}])[0].get("description", "Keine Beschreibung"),
            icon=data.get("weather", [{}])[0].get("icon", ""),
            temperature=data.get("main", {}).get("temp", 0.0)
        )
    except requests.exceptions.RequestException as e:
        print("Fehler bei der Wetterdaten-Anfrage:", e)
        return None
