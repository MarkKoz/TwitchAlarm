# Adapted from https://gist.github.com/THeK3nger/3624478
import os
import wave
from threading import Thread

import pyaudio


class WavePlayer(Thread):
    """A threaded class which plays a wave audio file using PyAudio.

    Can play audio on a loop.

    """

    CHUNK = 1024

    def __init__(self, path: str, loop: bool = True):
        """Initialise the player.

        Parameters
        ----------
        path: str
            The path to the wav file to play.

        loop: bool
            True if the audio should be looped.

        """
        super(WavePlayer, self).__init__()
        self.path = os.path.abspath(path)
        self.loop = loop

    def run(self):
        # Open the wave file and instantiates PyAudio.
        wf = wave.open(self.path, "rb")
        player = pyaudio.PyAudio()

        # Open an output stream.
        stream = player.open(
            format=player.get_format_from_width(wf.getsampwidth()),
            channels=wf.getnchannels(),
            rate=wf.getframerate(),
            output=True
        )

        # Play only once if not looping.
        if not self.loop:
            data = wf.readframes(self.CHUNK)

            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(self.CHUNK)

        # Playback loop
        while self.loop:
            data = wf.readframes(self.CHUNK)

            if len(data) == 0:  # Rewind when the file ends.
                wf.rewind()
                data = wf.readframes(self.CHUNK)

            stream.write(data)

        stream.close()
        wf.close()
        player.terminate()

    def play(self):
        """Start playback of the audio file.

        Notes
        -------
        Really an alias for start(), which starts the thread.

        """
        self.start()

    def stop(self):
        """Stop playback of the audio file."""
        self.loop = False
