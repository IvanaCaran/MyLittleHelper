from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Pfad zur Datei, die die Weckerzeiten speichert
ALARMS_FILE = "alarms.json"

# Funktion, um die Datei zu lesen
def load_alarms():
    if not os.path.exists(ALARMS_FILE):
        return []
    with open(ALARMS_FILE, "r") as file:
        return json.load(file)

# Funktion, um die Datei zu schreiben
def save_alarms(alarms):
    with open(ALARMS_FILE, "w") as file:
        json.dump(alarms, file)

@app.route("/alarms", methods=["GET"])
def get_alarms():
    alarms = load_alarms()
    return jsonify(alarms)

@app.route("/alarms", methods=["POST"])
def add_alarm():
    alarm = request.json
    alarms = load_alarms()
    alarms.append(alarm)
    save_alarms(alarms)
    return jsonify({"status": "success", "alarm": alarm})

@app.route("/alarms/<alarm_id>", methods=["DELETE"])
def delete_alarm(alarm_id):
    alarms = load_alarms()
    alarms = [alarm for alarm in alarms if alarm["id"] != alarm_id]
    save_alarms(alarms)
    return jsonify({"status": "success", "remaining_alarms": alarms})

@app.route("/alarms/<alarm_id>", methods=["PUT"])
def update_alarm(alarm_id):
    updated_alarm = request.json
    alarms = load_alarms()
    for alarm in alarms:
        if alarm["id"] == alarm_id:
            alarm.update(updated_alarm)
            break
    save_alarms(alarms)
    return jsonify({"status": "success", "updated_alarm": updated_alarm})

if __name__ == "__main__":
    app.run(debug=True)