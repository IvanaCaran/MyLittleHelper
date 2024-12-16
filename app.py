from flask import Flask, render_template, request, jsonify
from weather import get_lat_lon, get_current_weather
from news import get_latest_news
from dotenv import load_dotenv
import roslibpy
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


    # Connect to ROS
ros = roslibpy.Ros(host='localhost', port=9090)
ros.run()

# Define the ROS topic for velocity commands
cmd_vel_topic = roslibpy.Topic(ros, '/cmd_vel', 'geometry_msgs/Twist')

@app.route('/')
def index():
    return render_template('navigation.html')

@app.route('/move', methods=['POST'])
def move():
    direction = request.json.get('direction')

    
    twist = {
        'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0},
        'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}
    }

    if direction == 'forward':
        twist['linear']['x'] = 0.5
    elif direction == 'backward':
        twist['linear']['x'] = -0.5
    elif direction == 'left':
        twist['angular']['z'] = 0.5
    elif direction == 'right':
        twist['angular']['z'] = -0.5
    elif direction == 'stop':
        pass  # No movement

    
    cmd_vel_topic.publish(roslibpy.Message(twist))

    return jsonify({'status': 'success', 'direction': direction})

# Flask-Anwendung ausführen
if __name__ == "__main__":
    try:
        app.run(debug=True)
    finally:
        cmd_vel_topic.unadvertise()
        ros.terminate()
