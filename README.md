# Twitch Alarm
Sounds an alarm when a Twitch stream goes live.

### Requirements
* [Python 3.6](https://www.python.org/downloads/) or higher
* [requests](http://docs.python-requests.org/en/master/)
* [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/)
* [python-dateutil](https://dateutil.readthedocs.io/en/stable/)

### Configuration
A `JSON` file named `Configuration.json` in the same directory as `Main.py` is
used for configuration of the program. It has the following format:

```json
{
    "clientID": "",
    "channels": [
        "ChannelName1",
        "ChannelName2"
    ],
    "frequency": 60,
    "sound": "path/to/alarm/sound.wav"
}
```

* clientID - The Twitch application's client ID. Register the application
[here](https://dev.twitch.tv/dashboard/apps).
* channels - A list of the names of channels for which an alarm will sound when
live.
* frequency - The interval between live checks in seconds. Note the endpoint
for streams has a rate limit of 30 requests per minute.
* sound - Path to a `wav` audio file that will be used as the alarm sound.

### Usage
Run `Main.py`. If a channel goes live, an alarm will sound. The alarm will stop
after any key + <kbd>Enter</kbd> is pressed and the program will close; re-run
`Main.py` to restart the program.
