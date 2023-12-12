from services.classificator import *
from services.detector import *
from services.recognizer import *

from messenger import messenger

import sys
import cv2
import time
import threading
from config import config
from keyboard import read_key


class app:
    def __init__(self):
        self.serviceObjects = {
            "classificator": None,
            "detector": None,
            "recognizer": None,
        }
        self.services = []

        self.cameraStarted = False
        self.isExit = False

        self.messenger = messenger(config)

    def str2class(self, classname):
        return getattr(sys.modules[__name__], classname)

    def switchService(self, *services):
        self.services = []
        self.messenger.info(" ".join(services))
        for service in services:
            if self.serviceObjects[service] is None:
                self.serviceObjects[service] = self.str2class(service)(
                    self.messenger, config
                )
            self.services.append(service)

    def keyCapture(self):
        while True:
            try:
                key = read_key()
                self.service = None

                if self.cameraStarted is False:
                    self.messenger.info("Camera not started")
                    continue

                if key == 'c':  # key c
                    self.switchService("classificator", "detector")

                elif key == 'd':  # key d
                    self.switchService("detector")

                elif key == 'r':  # key r
                    self.switchService("recognizer")

                elif key == 'q':  # key q
                    self.exit()

                else:
                    self.messenger.warning("Invalid key")
                    continue

                time.sleep(0.1)
            except Exception as e:
                self.messenger.error(e)

    def main(self):
        self.messenger.info("Starting...")
        
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)
        self.cameraStarted = self.cap.isOpened()
        self.messenger.info("Camera started")

        while not self.cameraStarted:
            pass
        
        while not self.isExit:
            ret, frame = self.cap.read()
            if ret:
                if self.services != []:
                    for service in self.services:
                        self.serviceObjects[service].run(frame)
                        
                cv2.imshow('Inference', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
    def run(self):
        threading.Thread(target=self.keyCapture, daemon=True).start()
        self.main()

    def exit(self):
        self.isExit = True
        self.cap.release()
        cv2.destroyAllWindows()
        self.messenger.info("exit")
        self.messenger.waitDone(0.1)
        exit()


if __name__ == "__main__":
    app().run()
