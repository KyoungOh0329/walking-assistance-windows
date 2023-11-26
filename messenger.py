import os
import inspect
import logging
from glob import glob
from io import BytesIO

from gtts import gTTS
from string import punctuation
from pydub import AudioSegment
from pydub.playback import play

from labels import printLabels
from korean import korean


class messenger:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
        )

        self.LOGGER = logging.getLogger()

    def info(self, msg):
        caller = inspect.currentframe().f_back.f_globals["__name__"]
        if caller == "__main__":
            caller = "main"
        else:
            caller = caller.split(".")[-1]

        self.LOGGER.info(f"{caller} - {msg}")
        self.processing(msg, caller)  # Processing data by caller

    def error(self, msg):
        self.LOGGER.error(msg)

    def processing(self, msg, caller):
        if caller == "main":
            self.ttsPrepare(msg)

        elif caller == "detector":
            for data in msg:
                if data["conf"] > 0.6:
                    if data["labelName"] in printLabels:
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
        play(song)

        fileList = glob("./ffcache*")
        for filePath in fileList:
            os.remove(filePath)
