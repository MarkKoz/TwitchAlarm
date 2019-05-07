# https://gist.github.com/THeK3nger/3624478

from threading import Thread
import os
import wave

import pyaudio

class WavePlayer(Thread):
    """
    A threaded class which plays a wave audio file using PyAudio. Can play audio
    on a loop.
    """

    CHUNK = 1024

    def __init__(self, path: str, loop: bool = True):
        """
        Initialises the player.

        Parameters
        ----------
        path: str
            The path to the wav file to play.

        loop: bool
            Set to `True` to loop the audio; set to `False` otherwise.
        """
        super(WavePlayer, self).__init__()
        self.path = os.path.abspath(path)
        self.loop = loop

    def run(self):
        # Opens the wave file and instantiates PyAudio.
        wf = wave.open(self.path, "rb")
        player = pyaudio.PyAudio()

        # Opens an output stream.
        stream = player.open(
            format = player.get_format_from_width(wf.getsampwidth()),
            channels = wf.getnchannels(),
            rate = wf.getframerate(),
            output = True)

        # Plays only once if not looping.
        if not self.loop:
            data = wf.readframes(self.CHUNK)

            while len(data) > 0:
                stream.write(data)
                data = wf.readframes(self.CHUNK)

        # Playback loop
        while self.loop:
            data = wf.readframes(self.CHUNK)

            if len(data) == 0: # Rewinds when the file ends.
                wf.rewind()
                data = wf.readframes(self.CHUNK)

            stream.write(data)

        stream.close()
        wf.close()
        player.terminate()

    def play(self):
        """
        Starts playback of the audio file.

        Notes
        -------
        Is really an alias for self.start(), which starts the thread.

        Returns
        -------
        None
        """
        self.start()

    def stop(self):
        """
        Stops playback of the audio file.

        Returns
        -------
        None
        """
        self.loop = False
