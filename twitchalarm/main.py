from typing import Dict
import datetime
import json
import time

from dateutil import parser
import requests

from audio import WavePlayer

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
        timestamp = datetime.datetime.now().replace(microsecond = 0).isoformat()
        print(f"[{timestamp}] Checking if live...")

        try:
            streams = getStreams(channels)
            data = streams["data"]

            if data:
                onLive(data)
                live = True
                break
        except (requests.exceptions.HTTPError,
                requests.exceptions.Timeout) as e:
            print(e.args[0])
            continue

def onLive(streams):
    for s in streams:
        timestamp = datetime.datetime.now().replace(microsecond = 0).isoformat()
        name = getDisplayName(s["user_id"])
        started = parser.parse(s["started_at"]).\
            astimezone(tz = None).replace(tzinfo = None).isoformat()
        print(f"[{timestamp}] {name} went live at {started}")

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
