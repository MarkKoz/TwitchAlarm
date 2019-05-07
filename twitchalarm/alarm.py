import datetime
import time

import requests
from dateutil import parser

from twitchalarm.audio import WavePlayer

TWITCH_API = "https://api.twitch.tv/helix"


def get_streams(channels, client_id):
    response = requests.get(
        f"{TWITCH_API}/streams",
        params={
            "type": "live",
            "user_login": channels
        },
        headers={"Client-ID": client_id}
    )
    response.raise_for_status()

    return response.json()


def get_display_name(user_id, client_id):
    response = requests.get(
        f"{TWITCH_API}/users",
        params={"id": user_id},
        headers={"Client-ID": client_id}
    )
    response.raise_for_status()
    data = response.json()["data"]

    if not data:
        # TODO: Throw an exception?
        return ""

    return data[0]["display_name"]


def poll_stream_status(config):
    live = False

    while not live:
        time.sleep(config.frequency)
        timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
        print(f"[{timestamp}] Checking if live...")

        try:
            streams = get_streams(config.channels, config.client_id)
            data = streams["data"]

            if data:
                on_live(data, config.client_id, config.sound)
                live = True
                break
        except (requests.HTTPError, requests.Timeout) as e:
            print(e.args[0])
            continue


def on_live(streams, client_id, sound):
    for s in streams:
        timestamp = datetime.datetime.now().replace(microsecond=0).isoformat()
        name = get_display_name(s["user_id"], client_id)
        started = parser.parse(s["started_at"])
        started = started.astimezone(tz=None).replace(tzinfo=None).isoformat()
        print(f"[{timestamp}] {name} went live at {started}")

    play_alarm(sound)


def play_alarm(sound_path):
    sound = WavePlayer(sound_path)
    sound.play()

    input("Enter anything to stop the alarm.")
    sound.stop()
