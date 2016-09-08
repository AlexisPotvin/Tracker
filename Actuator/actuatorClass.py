__author__ = 'User'

import GLOBAL
import threading
import time


class Actuator():
    # calss constructor
    def __init__(self):
        self._stop = threading.Event()
        self.loopFrequency = 1  # Hz
        threading.Thread.__init__(self, target=self.main)
        self.__lastLoopTS = time.time()  # time stamp of the beginning of the last main loop



    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def main(self):
        # do shit
        while not(self.stopped()):
            if time.time() > self.__lastLoopTS + (1/self.loopFrequency):

                print "do this now"