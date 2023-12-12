from easyocr import Reader


class recognizer:
    def __init__(self, messenger, config):
        self.messenger = messenger
        self.reader = Reader(["ko", "en"], gpu=True)

    def run(self, frame):
        result = self.reader.readtext(frame, detail=0)
        self.messenger.info(result)
