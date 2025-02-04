import time
import threading


class Timer:
    def __init__(self, name, duration, sound, repeat=False):
        self.name = name
        self.duration = duration
        self.sound = sound
        self.repeat = repeat
        self.active = True

    def start(self):
        def run_timer():
            while self.active:
                print(f"Timer '{self.name}' läuft für {self.duration} Sekunden.")
                time.sleep(self.duration)
                print(f"Sound '{self.sound}' wird abgespielt!")
                time.sleep(15)  # Ton spielt für 15 Sekunden

                if not self.repeat:
                    break

        threading.Thread(target=run_timer).start()

    def stop(self):
        self.active = False
        print(f"Timer '{self.name}' wurde gestoppt.")
