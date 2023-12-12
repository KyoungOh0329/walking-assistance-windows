import os
import time
import inspect
import logging
from glob import glob
from io import BytesIO

from gtts import gTTS
from threading import Thread
from string import punctuation
from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio

from korean import korean


class messenger:
    def __init__(self, config):
        self.config = config

        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )
        self.LOGGER = logging.getLogger()

        self.playbacks = []

    def info(self, msg, force=False):
        caller = inspect.currentframe().f_back.f_globals["__name__"]
        if caller == "__main__":
            caller = "main"
        else:
            caller = caller.split(".")[-1]

        if force:
            self.forceStop()

        self.LOGGER.info(f"{caller}({force}) - {msg}")
        self.processing(msg, caller)  # Processing data by caller

    def warning(self, msg):
        self.LOGGER.warning(msg)

    def error(self, msg):
        self.LOGGER.error(msg)

    def processing(self, msg, caller):
        if caller == "main":
            self.ttsPrepare(msg)

        elif caller == "detector":
            for data in msg:
                if data["conf"] > 0.6:
                    if data["labelName"] in self.config["detector"]["printLabels"]:
                        self.LOGGER.info(f"{data['labelName']} {data['position']}")
                        self.ttsPrepare(f"{data['labelName']} {data['position']}")

        elif caller == "recognizer":
            if msg == []:
                return

            self.ttsPrepare("".join(msg))

        elif caller == "classificator":
            self.ttsPrepare(msg)

    # Translate English to Korean with punctuation removal
    def ttsPrepare(self, msg):
        en = ""
        ko = ""
        last = "en"

        # 한글화
        if self.config["translate"]:
            for word in korean:
                msg = msg.replace(word, korean[word])

        for char in msg:
            if char not in punctuation:
                if char.encode().isalpha():
                    en += char
                    last = "en"
                elif char.isalpha():
                    ko += char
                    last = "ko"
                else:
                    if last == "en":
                        en += char
                    else:
                        ko += char

        if en.strip() != "":
            self.tts(en, "en")

        if ko.strip() != "":
            self.tts(ko, "ko")

    def tts(self, msg, lang="en"):
        tts = gTTS(text=msg, lang=lang)

        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)

        song = AudioSegment.from_file(fp, format="mp3")

        self.waitDone()
        self.playbacks.append(_play_with_simpleaudio(song))

        fileList = glob("./ffcache*")
        for filePath in fileList:
            os.remove(filePath)

    def isPlaying(self):
        if self.playbacks == []:
            return False

        return self.playbacks[-1].is_playing()

    def waitDone(self, wait=None):
        if self.isPlaying():
            if wait is not None:
                time.sleep(wait)
            self.playbacks[-1].wait_done()
            self.playbacks = []

    def forceStop(self):
        if self.isPlaying():
            self.playbacks[-1].stop()
