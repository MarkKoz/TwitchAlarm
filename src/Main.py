from typing import Dict
import json
import time

import requests
from Audio import WavePlayer

config = dict()

urlBase = "https://api.twitch.tv/helix/"

def getStreams(channels):
    response = requests.get(f"{urlBase}streams",
                            params = {
                                "type": "live",
                                "user_login": [c for c in channels]
                            },
                            headers = {"Client-ID": config["clientID"]})
    response.raise_for_status()

    return response.json()

def getDisplayName(userID):
    response = requests.get(f"{urlBase}users",
                            params = {"id": userID},
                            headers = {"Client-ID": config["clientID"]})
    response.raise_for_status()
    data = response.json()["data"]

    if not data:
        # TODO: Throw an exception?
        return ""

    return data[0]["display_name"]

def loadConfig() -> Dict:
    with open("Configuration.json") as file:
        return json.load(file)

def checkLive(channels):
    live = False

    while not live:
        time.sleep(config["frequency"])
        print("Checking if live...")

        try:
            streams = getStreams(channels)
            data = streams["data"]

            if data:
                onLive(data)
                live = True
                break
        except requests.exceptions.HTTPError as e:
            print(e.args[0])
            continue

def onLive(streams):
    for s in streams:
        name = getDisplayName(s["user_id"])
        started = s["started_at"]
        print(f"{name} went live at {started}")

    playAlarm()

def playAlarm():
    sound = WavePlayer(config["sound"])
    sound.play()

    input("Enter anything to stop the alarm.")
    sound.stop()

def main():
    checkLive(config["channels"])

if __name__ == "__main__":
    config = loadConfig()
    main()
