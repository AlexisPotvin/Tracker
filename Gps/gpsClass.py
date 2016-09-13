
import threading
import time
import os
import gps


class GpsClass(threading.Thread):

    def __init__(self):
        """ Class threading setup"""
        self.loopFrequency = 10  # Hz
        self._stop = threading.Event()
        threading.Thread.__init__(self, target=self.main)
        self.__lastLoopTS = time.time()  # time stamp of the beginning of the last main loop
        self.daemon = True

        """Class variables """
        self.rawLat = 0
        self.rawLong = 0
        self.rawAlt = 0

        """Required for average calculation"""
        self.sumLat = 0
        self.sumLong = 0
        self.sumAlt = 0
        """ I stand for increment value"""
        self.sumAltI = 0
        self.sumLatI = 0
        self.sumLongI = 0

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
                self.sumLat += report.alt
                self.sumLatI += 1

            if hasattr(report, 'lon'):
                self.rawLong = report.lon
                self.sumLong += report.Long
                self.sumLongI += 1

            if hasattr(report, 'lat'):
                self.rawAlt = report.lat
                self.sumAlt += report.Alt
                self.sumAltI += 1

    def avgLat(self):
        try:
            return self.sumLat/self.sumLatI
        except ZeroDivisionError:
            return None

    def avgLong(self):
        try:
            return self.sumLong/self.sumLongI
        except ZeroDivisionError:
            return None

    def avgAlt(self):
        try:
            return self.sumAlt/self.sumAltI
        except ZeroDivisionError:
            return None

    def main(self):
        self.initGpsd()
        while not(self.stopped()):
            if time.time() > self.__lastLoopTS + (1/self.loopFrequency):
                self.__lastLoopTS = time.time()

                print time.time()
                print ("shit was done")
