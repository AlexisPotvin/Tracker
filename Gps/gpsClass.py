__author__ = 'User'
import GLOBAL
import threading
import time
import os
import gps

class GpsClass(threading.Thread):
    # calss constructor
    def __init__(self):
        self._stop = threading.Event()
        self.loopFrequency = 10  # Hz
        threading.Thread.__init__(self, target=self.main)
        self.__lastLoopTS = time.time()  # time stamp of the beginning of the last main loop
        self.daemon = True
        self.rawLat = 0
        self.rawLong = 0
        self.rawAlt = 0

    def __del__(self):
        self.stop()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def initGpsd (self):
        os.system("sudo killall gpsd")
        os.system("sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock")
        self.gpsSession = gps.gps("localhost", "2947")
        self.gpsSession.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

    def pullGpsCoordinates(self):
        report = self.gpssession.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'alt'):
                self.rawLat = report.alt
            if hasattr(report, 'lon'):
                self.rawLong = report.lon
            if hasattr(report, 'lat'):
                self.rawAlt = report.lat

    def main (self):
        self.initGpsd()
        while not(self.stopped()):
            if time.time() > self.__lastLoopTS + (1/self.loopFrequency):
                self.__lastLoopTS = time.time()

                print time.time()
                print ("shit was done")
