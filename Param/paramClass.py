__author__ = 'User'
import GLOBAL
import threading
import time


class Param(threading.Thread):
    # calss constructor
    def __init__(self):
        self._stop = threading.Event()
        self.loopFrequency = 1  # Hz
        threading.Thread.__init__(self, target=self.main)
        self.__lastLoopTS = time.time()  # time stamp of the beginning of the last main loop

    def __del__(self):
        self.stop()


    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def main(self):
        # do shit
        while not(self.stopped()):
            if time.time() > self.__lastLoopTS + (1/self.loopFrequency):

                self.__lastLoopTS = time.time()

                print time.time()
                print ("shit was done")









