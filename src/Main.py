from typing import Dict
import time
import json

from twitch import TwitchClient
from Audio import WavePlayer
from requests import exceptions

config = dict()
client = TwitchClient()

def loadConfig() -> Dict:
    with open("Configuration.json") as file:
        return json.load(file)

def checkLive(channels):
    channels = client.users.translate_usernames_to_ids(channels)
    live = False

    while not live:
        time.sleep(config["frequency"])
        print("Checking if live...")

        for c in channels:
            try:
                stream = client.streams.get_stream_by_user(c.id)
            except exceptions.HTTPError as e:
                print(e.args[0])
                continue

            if stream:
                onLive(stream)
                live = True
                break

def onLive(stream):
    name = stream["channel"]["display_name"]
    created = stream["created_at"]
    print(f"{name} went live at {created}")
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
    client = TwitchClient(config["clientID"])
    main()
