
import os
from datetime import datetime, timedelta
import json
from playsound import playsound

ALARMS_FILE = "alarms.json"

def load_alarms():
    if os.path.exists(ALARMS_FILE):
        with open(ALARMS_FILE, "r") as file:
            return json.load(file)
    return []

def save_alarms(alarms):
    with open(ALARMS_FILE, "w") as file:
        json.dump(alarms, file)

def add_alarm(time, label):
    alarms = load_alarms()
    alarms.append({"time": time, "label": label, "enabled": True})
    save_alarms(alarms)

def delete_alarm(index):
    alarms = load_alarms()
    if 0 <= index < len(alarms):
        del alarms[index]
        save_alarms(alarms)

def toggle_alarm(index, enabled):
    alarms = load_alarms()
    if 0 <= index < len(alarms):
        alarms[index]["enabled"] = enabled
        save_alarms(alarms)

def check_alarms():
    alarms = load_alarms()
    current_time = datetime.now().strftime("%H:%M")
    for alarm in alarms:
        if alarm["enabled"] and alarm["time"] == current_time:
            play_sound()
            alarm["enabled"] = False
    save_alarms(alarms)

def play_sound():
    os.system("mpg123 -q alarm_sound.mp3")