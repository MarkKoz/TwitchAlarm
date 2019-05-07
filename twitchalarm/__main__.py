import os
from argparse import ArgumentParser
from pathlib import Path

from twitchalarm.alarm import poll_stream_status

parser = ArgumentParser(
    prog="twitch-alarm",
    description="Sound an alarm when a Twitch channel goes live."
)
parser.add_argument(
    "channels",
    nargs="+",
    help="Channels to check if live."
)
parser.add_argument(
    "--client_id",
    required=False if "TWITCH_CLIENT_ID" in os.environ else True,
    default=os.environ.get("TWITCH_CLIENT_ID"),
    help="Twitch API client ID. Required unless specified with the environment"
         "variable TWITCH_CLIENT_ID."
)
parser.add_argument(
    "--frequency", "-f",
    type=int,
    default=60,
    help="Frequency, in seconds, at which to check if a channel is live."
)
parser.add_argument(
    "--sound", "-s",
    type=lambda p: Path(p).resolve(True),
    help="Path to the sound file to use for the alarm. Supports only wav files."
)
args = parser.parse_args()

poll_stream_status(args)
