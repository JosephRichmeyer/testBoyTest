from gps import *
import time

class Sensors:
    def __init__(self, wind1, compass1, gps1, gps2):
        self.wind1 = wind1
        self.compass1 = compass1
        self.gps1 = gps1
        self.gps2 = gps2


    def getLat():
        gpsLog = []
        gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
        for i in range(5):
            report = gpsd.next()
            if report['class'] == 'TPV':
                gpsCheck = getattr(report,'lat',0.0)
                if ((0.0 != gpsCheck) and (gpsCheck is not None)):
                    #print (gpsCheck)
                    gpsLog.append(gpsCheck)
        return gpsLog[-1]
                    
            #else:
                #getLat()
                

    def getLong():
        gpsLog2 = []
        gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE)
        for i in range(5):
            report = gpsd.next()
            if report['class'] == 'TPV':
                gpsCheck = getattr(report,'lon',0.0)
                if ((0.0 != gpsCheck) and (gpsCheck is not None)):
                    #print (gpsCheck)
                    gpsLog2.append(gpsCheck)
        return gpsLog2[-1]


    #takes wind direction in degrees from aenemometer every second, calculates in quadrant (18 quadrants of 20degrees)
    windQuadLog = []

    #get current wind quad and return it with a function
    def windLogger(wind1):
        if (len(windQuadLog) < 60):
            windQuadLog.append(toQuadrant(wind1))
        else:
            #deletes the first entry in the logger and adds current wind speed to the end
            del windLog[0]
            windQuadLogg.append(toQuadrant(wind1))

    def getWindQuad():
        #below calculates a new list based on a weighted average of the previous wind quadrants and gets the mode for the windspeed
        #first 20 seconds weighted 1, 2nd weighted x2 and 3rd (most recent) weighted x3
        weightedWindLog = windQuadrantLog + windQuadrantLog[20:39] + windQuadrantLog[40:59] + windQuadrantLog[40:59]
        try:
            return mode(weightedWindLog)
        except statistics.StatisticsError: #StatisticsError if there isnt a mode
            print ("Mode not calulated")
            time.sleep(5)

    def toQuadrant(windSource):
        roundWind = round(windSource)
        if ((roundWind > 349) or (roundWind <= 9)):
            return 1
        elif ((roundWind > 9) and (roundWind <= 29 )):
            return 2
        elif ((roundWind > 29) and (roundWind <= 49 )):
            return 3
        elif ((roundWind > 49) and (roundWind <= 69 )):
            return 4
        elif ((roundWind > 69) and (roundWind <= 89 )):
            return 5
        elif ((roundWind > 89) and (roundWind <= 109 )):
            return 6
        elif ((roundWind > 109) and (roundWind <= 129 )):
            return 7
        elif ((roundWind > 129) and (roundWind <= 149 )):
            return 8
        elif ((roundWind > 149) and (roundWind <= 169 )):
            return 9
        elif ((roundWind > 169) and (roundWind <= 189 )):
            return 10
        elif ((roundWind > 189) and (roundWind <= 209 )):
            return 11
        elif ((roundWind > 209) and (roundWind <= 229 )):
            return 12
        elif ((roundWind > 229) and (roundWind <= 249 )):
            return 13
        elif ((roundWind > 249) and (roundWind <= 269 )):
            return 14
        elif ((roundWind > 269) and (roundWind <= 289 )):
            return 15
        elif ((roundWind > 289) and (roundWind <= 309 )):
            return 16
        elif ((roundWind > 309) and (roundWind <= 329 )):
            return 17
        elif ((roundWind > 329) and (roundWind <= 349 )):
            return 18