import datetime
import time

from dateutil import parser
import requests

from twitchalarm.audio import WavePlayer

urlBase = "https://api.twitch.tv/helix/"

def getStreams(channels, client_id):
    response = requests.get(f"{urlBase}streams",
                            params = {
                                "type": "live",
                                "user_login": [c for c in channels]
                            },
                            headers = {"Client-ID": client_id})
    response.raise_for_status()

    return response.json()

def getDisplayName(userID, client_id):
    response = requests.get(f"{urlBase}users",
                            params = {"id": userID},
                            headers = {"Client-ID": client_id})
    response.raise_for_status()
    data = response.json()["data"]

    if not data:
        # TODO: Throw an exception?
        return ""

    return data[0]["display_name"]

def checkLive(config):
    live = False

    while not live:
        time.sleep(config.frequency)
        timestamp = datetime.datetime.now().replace(microsecond = 0).isoformat()
        print(f"[{timestamp}] Checking if live...")

        try:
            streams = getStreams(config.channels, config.client_id)
            data = streams["data"]

            if data:
                onLive(data, config.client_id, config.sound)
                live = True
                break
        except (requests.exceptions.HTTPError,
                requests.exceptions.Timeout) as e:
            print(e.args[0])
            continue

def onLive(streams, client_id, sound):
    for s in streams:
        timestamp = datetime.datetime.now().replace(microsecond = 0).isoformat()
        name = getDisplayName(s["user_id"], client_id)
        started = parser.parse(s["started_at"]).\
            astimezone(tz = None).replace(tzinfo = None).isoformat()
        print(f"[{timestamp}] {name} went live at {started}")

    playAlarm(sound)

def playAlarm(sound_path):
    sound = WavePlayer(sound_path)
    sound.play()

    input("Enter anything to stop the alarm.")
    sound.stop()
