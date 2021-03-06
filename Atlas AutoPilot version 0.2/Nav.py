import math
import geopy
import geopy.distance
from geopy.distance import geodesic

#location data: ideally, the gps module will use decimal degrees instead of degrees, minutes, and seconds
#initializing classes for the current location - will come from gps feed
# we actually just need to convert this to decimal degrees so that
#use a linux gps usb reciever
class Navigation:
     #converts degrees, minutes, and seconds to decimal degrees and makes West and South cardinals negative
    def convertToDecimal(cardinal, degrees, minutes, seconds):
        decimalGps = degrees + (minutes / 60) + (seconds / 3600)
        if ("N" == cardinal.upper()):
            return decimalGPS
        elif ("S" == cardinal.upper()):
            return -decimalGPS
        elif ("W" == cardinal.upper()):
            return -decimalGPS
        elif ("E" == cardinal.upper()):
            return decimalGPS
        else:
            print ("Error inputting cardinal gps character into convertToDecimal function.")


    #this grabs data from the gps receiver and updates it to the class instance every 5 seconds (timer job)
    #def updateLocation():

    #takes two location parameters in the form of gps decimal (lat, long)  and returns the distance between them
    def getDistance(loc1, loc2):
        return ((geodesic(loc1,loc2)).miles)

    #this will be called when the target heading is not within 45degrees of each side of the wind bearing
    def tack():
        rudderMain.rudderAngle = 0
        return True

    #takes two location parameters in the form of gps decimal (lat, long) adn returns the target compass heading using haversine formula
    def getHeading(pointA,pointB):
        if (type(pointA) != tuple) or (type(pointB) != tuple):
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(pointA[0])
        lat2 = math.radians(pointB[0])
        diffLong = math.radians(pointB[1] - pointA[1])
        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
                * math.cos(lat2) * math.cos(diffLong))
        initial_bearing = math.atan2(x, y)
        # Now we have the initial bearing but math.atan2 return values
        # from -180° to + 180° which is not what we want for a compass bearing
        # The solution is to normalize the initial bearing as shown below
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = (initial_bearing + 360) % 360
        return compass_bearing
