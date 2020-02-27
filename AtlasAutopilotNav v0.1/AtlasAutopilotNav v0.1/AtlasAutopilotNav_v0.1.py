import threading
import concurrent.futures
import sqlite3
from sqlite3 import Error
import tkinter
from tkinter import *
import random
import time
import math
#import pyowm
import requests
import json
import geopy
import geopy.distance
from geopy.distance import geodesic
from collections import Counter
from statistics import mode

#https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
#perhaps use this for the maps
#from OSMPythonTools.api import Api

#everything in the craft software has to work with only infrequent updates through data link
#no api or library can use internet data

#class jobThreader:
    #while true:


class craftInfo:
    def __init__(self, towing, craftID, active, tacking):
        self.towing = towing
        self.craftID = craftID
        self.active = active
        self.tacking = tacking
    towing = False
    craftID = 1313
    active = True
    tacking = False

#class jobTimer:
#rudder Steer() runs every .1 seconds
#waypoint check runs every 60 seconds
#windLogger runs once per second
#sailAdjuster runs every 60 seconds
#calls sailAdjust

#class dataBase:
#    def __init__(self, curs, conn):

#        self.conn = conn
#        self.curs = curs


#    def connectDB():
#        try:
#            conn = sqlite3.connect('AtlasLog.db')
#        except:
#            print("Unable to connect to database.")

#    curs = conn.cursor()

#    def createTable():
#        try:
#            curs.execute('''CREATE TABLE IF NOT EXISTS log1313
#            (Date text, Time text, CraftID int,  ''')
#        except:
#            print ("Table already created")

#    def createTableWaypoints():
#        try:
#            curs.execute('''CREATE TABLE IF NOT EXISTS Waypoint (Number int, Latitude text, Longitude text, Completed boolean)''')
#        except:
#            print("Table Waypoint not created")


#    #below is run once per second
#    def dataLog(time, speed, rudder, aftWin, forWin):
#        curs.execute("INSERT INTO stocks VAlUES  (')")


#location data: ideally, the gps module will use decimal degrees instead of degrees, minutes, and seconds
#initializing classes for the current location - will come from gps feed
# we actually just need to convert this to decimal degrees so that 
#use a linux gps usb reciever
class Navigation:
    def __init__(self, latCurrent, longCurrent, latTarget, longTarget, Heading, targetHeading, targetDistance, 
                 latCRNTDecimal, longCRNTDecimal, latTGTDecimal, longTGTDecimal):
        self.latCurrent = latCurrent
        self.longCurrent = longCurrent
        self.latTarget = latTarget
        self.longTarget = longTarget
        self.Heading = Heading
        self.targetHeading = targetHeading
        self.latCRNTDecimal = latCRNTDecimal
        self.longCRNTDecimal = longCRNTDecimal
        self.latTGTDecimal = latTGTDecimal
        self.longTGTDecimal = longTGTDecimal

    #location feed from gps
    latCurrent = ["N", 38, 5, 9.37]
    longCurrent= ["W", 90, 34, 46.21]
    #initializing classes for target waypoint
    latTarget = ["N", 43, 47, 5.09]
    longTarget= ["W", 86, 26, 22.56]
    Heading = 0
    targetHeading = 0

     #converts degrees, minutes, and seconds to decimal degrees and makes West and South cardinals negative
    def convertToDecimal(cardinal, degrees, minutes, seconds):
        decimalGps = degrees + (minutes / 60) + (seconds / 3600)
        if ("N" == cardinal.upper()):
            latDecimal = decimalGPS
            print (latDecimal)
        elif ("S" == cardinal.upper()):
            latDecimal = -decimalGPS
        elif ("W" == cardinal.upper()):
            longDecimal = -decimalGPS
        elif ("E" == cardinal.upper()):
            longDecimal = decimalGPS
        else:
            print ("Error inputting cardinal gps character into convertToDecimal function.")

        print (decimalGps)
        return decimalGps

    #this grabs data from the gps receiver and updates it to the class instance every 5 seconds (timer job)
    #def updateLocation():

    #takes two location parameters in the form of gps decimal (lat, long)  and returns the distance between them
    def getDistance(loc1, loc2):
        return ((geodesic(loc1,loc2)).miles)

    def tack():
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



class Sensors:
    def __init__(self, wind1, compass1, gps1, gps2):
        self.wind1 = wind1
        self.compass1 = compass1
        self.gps1 = gps1
        self.gps2 = gps2

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


class Rudder:
    #pass in compass heading rounded to nearest degree
    rudderAngle = 0
    #rudderRange = [-45,45] -45 means to turn left, +45 is right turn
    def Steer(heading, tgtHeading):
        if (heading != tgtHeading):

            binHeading = Rudder.degreeToBin(heading)
            binTGTHeading = Rudder.degreeToBin(tgtHeading)
            #this divides up the results 
            if (binHeading < binTGTHeading): #checks if a right turn is nessecary
                Rudder.rudderAngle = Rudder.rudderMinMax(binTGTHeading - binHeading)
                return Rudder.rudderAngle
            else: #executes a left turn
                Rudder.rudderAngle = Rudder.rudderMinMax(-(binHeading- binTGTHeading))
                return Rudder.rudderAngle

    #this function converts compass input (0:359) and transforms it to (-180:180)
    def degreeToBin(dg):
        rndDG = round(dg)
        if ((rndDG >= 0) and (rndDG <= 180)):
            return rndDG
        elif ((rndDG <= 359 ) and (rndDG > 180)) :
            return (rndDG - 360)
        elif (rndDG == 360):
            return 0

    #This transforms input from steer() on nessecary degree correction and returns the rudder max angles
    def rudderMinMax(rud):
        if (rud == 0):
            return 0
        elif ((rud > 0) and (rud > 45)):
            return 45
        elif ((rud > 0) and (rud <= 45)):
            return rud
        elif ((rud < 0) and (rud >= -45)):
            return rud
        elif ((rud < 0) and (rud < -45)):
            return -45


class sailControl:
    def __init__(self, aftWinch, forwardWinch):
        self.aftWinch = aftWinch
        self.forwardWinch = forwardWinch
    forwardWinch = 0
    aftWinch = 0
    def sailAdjust(winch):
        #adjusts winches to paramenter angle (or quadrant)
        try:
            quad = Sensors.getWindQuad()
        except:
            print("Mode not returned.")
            time.sleep(10)
            sailAdjust(winch)

        if ((quad == 1) or (quad == 2) or (quad == 3) or (quad == 17) or (quad == 18)):
            print ("Wind insufficent, tacking needed:")
            return "Tacking initialized" #for test
            #tack() #create tacking algorithm with tack distance
        elif (quad == 4) or (quad == 16):
            return 10
            if (winch == "forward"):
                fowardAdjust(10) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(10) #with parameter
        elif (quad == 5) or (quad == 15):
            return 26
            if (winch == "forward"):
                fowardAdjust(26) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(26) #with parameter
        elif (quad == 6) or (quad == 14):
            return 42
            if (winch == "forward"):
                fowardAdjust(42) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(42) #with parameter
        elif (quad == 7) or (quad == 13):
            return 58
            if (winch == "forward"):
                fowardAdjust(58) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(58) #with parameter
        elif (quad == 8) or (quad == 12):
            return 74
            if (winch == "forward"):
                fowardAdjust(74) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(74) #with parameter
        elif ((quad == 10) or (quad == 9) or (quad == 11)):
            return 90
            if (winch == "forward"):
                fowardAdjust(90) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(90) #with parameter

    def forwardAdjust(angle): #this will get current sail angle and make winch timing and power adjustments for the new parameter
        if (forwardWinch != angle):
            forwardWinch = angle
            print ("Forward sail winch adjusted to " + angle + " degrees.")
            #add code for winch later

    def aftAdjust(angle): #this will get current sail angle and make winch timing and power adjustments for the new parameter
        if (aftdWinch != angle):
            aftWinch = angle
            print ("Aft winch adjusted to " + angle + "degrees.")
            #add code for winch later

#BELOW IS ALL FOR DEMONSTRATION TESTING
class testing:
    #methods below
    def testRudder():
        #for i in range(20):
        while True:
            tgtHead = random.randint(1,360)
            head = random.randint(1,360)
            print ("With heading " + str(head) + " and targetHeading " + str(tgtHead))
            print ("Rudder angle Calculated is: " + str(Rudder.Steer(head, tgtHead)))

            
    #this is the most complicated test. Here, we pull weather data from openweatherapp.com using inputted gps coordinates
    #with the call, we can get wind direction
    #then, we pass wind direction into our aenomometer parameter and use the gui/print out the proper sail pattern for that wind direction
    def testNavigation(latE, longE, typ):
        #openweather api key 4fa24bbb6c5e312bfc97c96b82195b11
        #https://stackoverflow.com/questions/1474489/python-weather-api
        api_key= "4fa24bbb6c5e312bfc97c96b82195b11"
        base_url =("http://api.openweathermap.org/data/2.5/weather?lat="+latE+"&lon="+longE+"&appid="+ api_key)
        response = requests.get(base_url)
        #converts response object to python format
        x = response.json()
        if x["cod"] != "404":
            y = x["wind"]
            openWindSpeed = y["speed"]
            openWindDir = y["deg"]
            if (typ == "speed"):
                return openWindSpeed
            elif (typ == "direction"):
                return openWindDir
            else:
                print("Failure to get OpenWeather API call")

class testingGUI:
    #this needs to take two locations as inputs, start and target
    #and an input as current craft heading
    #using location, gets the wind direction from openmaps
    #then prints the target heading, wind direction and speed at the location, 
    def __init__(self, master):
        self.master = master
        master.title("Atlas Autopilot GUI Tester")
        self.label = Label(master, text="This is a snapshot of the Atlas autpilot functions based upon sensor inputs.")
        self.label.pack()
        self.label2 = Label(master, text="Instead of anemometer input, real weather data is downloaded from OpenWeather.")
        self.label2.pack()

        self.latitude_label = Label(master, text="Enter the latitude of the craft below in decimal format:")
        self.latitude_label.pack()

        self.lat_entry = Entry(master, bd=2)
        self.lat_entry.pack()

        self.longitude_label = Label(master, text="Enter the longitude of the craft below in decimal format:")
        self.longitude_label.pack()

        self.long_entry = Entry(master, bd=2)
        self.long_entry.pack()

        self.latitude_target = Label(master, text="Enter the latitude of the target waypoint:")
        self.latitude_target.pack()

        self.lat_entryTGT = Entry(master, bd=2)
        self.lat_entryTGT.pack()

        self.longitude_target = Label(master, text="Enter the longitude of the target waypoint:")
        self.longitude_target.pack()

        self.long_entryTGT = Entry(master, bd=2)
        self.long_entryTGT.pack()

        self.heading_label = Label(master, text="Enter the current heading of the craft below:")
        self.heading_label.pack()

        self.heading = Entry(master, bd=2)
        self.heading.pack()

        self.navButton = Button(master, text="Get Navigation", command=self.getNav)
        self.navButton.pack()

        self.windSpeed = Label(master, text="Wind speed at craft location (miles per hour):")
        self.windSpeed.pack()
        self.windSpeedtxt = Text(master, height=1, width=10)
        self.windSpeedtxt.insert(INSERT,"")
        self.windSpeedtxt.pack()

        self.windHeading = Label(master, text="Wind heading at craft location (degrees):")
        self.windHeading.pack()
        #display wind heading here
        self.windHead = Text(master, height=1, width=10)
        self.windHead.insert(INSERT,"")
        self.windHead.pack()

        self.sailAngle = Label(master, text="Angle of sail changed to (degrees):")
        self.sailAngle.pack()

        self.sailAng = Text(master, height=1, width=10)
        self.sailAng.insert(INSERT,"")
        self.sailAng.pack()

        self.rudderAng = Label(master, text="Angle of the rudder changed to (degrees):")
        self.rudderAng.pack()
        
        self.rudderAngle = Text(master, height=1, width=10)
        self.rudderAngle.insert(INSERT,"")
        self.rudderAngle.pack()

        self.targetHeading =Label(master, text="New heading/bearing target (degrees):")
        self.targetHeading.pack()

        self.targetHead = Text(master, height=1, width=10)
        self.targetHead.insert(INSERT,"")
        self.targetHead.pack()

        self.distanceLabel = Label(master, text="Distance to target waypoint (miles):")
        self.distanceLabel.pack()

        self.distance = Text(master, height=1, width=10)
        self.distance.insert(INSERT,"")
        self.distance.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def getNav(self):
        #initializes variables
        lat1 = self.lat_entry.get()
        long1 = self.long_entry.get()
        lat2 = self.lat_entryTGT.get()
        long2 = self.long_entryTGT.get()
        head1 = self.heading.get()
        dst1 = (float(lat1), float(long1))
        dst2 = (float(lat2), float(long2))
        print(head1)
        nav1 = Navigation.getHeading(dst1,dst2)
        #deletes fields
        self.distance.delete('1.0', END)
        self.targetHead.delete('1.0', END)
        self.windSpeedtxt.delete('1.0', END)
        self.windHead.delete('1.0',END)
        self.sailAng.delete('1.0',END)
        self.rudderAngle.delete('1.0', END)

        #updates fields
        self.distance.insert(INSERT,Navigation.getDistance(dst1,dst2))
        self.targetHead.insert(INSERT, str(nav1))
        self.windHead.insert(INSERT, testing.testNavigation(lat1,long1,"direction"))
        self.windSpeedtxt.insert(INSERT, (2.23694 * (testing.testNavigation(lat1,long1,"speed"))))
        windHeadBin = Rudder.degreeToBin(testing.testNavigation(lat1,long1,"direction"))
        tgtHeadBin = Rudder.degreeToBin(float(nav1))
        self.sailAng.insert(INSERT, testingGUI.windTestQuad(Sensors.toQuadrant(abs(tgtHeadBin-windHeadBin)))) 

        correction = Rudder.degreeToBin(float(nav1)) - Rudder.degreeToBin(float(head1))
        self.rudderAngle.insert(INSERT, Rudder.rudderMinMax(correction))

    def windTestQuad(quad):
        if ((quad == 1) or (quad == 2) or (quad == 3) or (quad == 17) or (quad == 18)):
            print ("Wind insufficent, tacking needed:")
            return "Tacking initialized" #for test
            #tack() #create tacking algorithm with tack distance
        elif (quad == 4) or (quad == 16):
            return 10
            if (winch == "forward"):
                fowardAdjust(10) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(10) #with parameter
        elif (quad == 5) or (quad == 15):
            return 26
            if (winch == "forward"):
                fowardAdjust(26) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(26) #with parameter
        elif (quad == 6) or (quad == 14):
            return 42
            if (winch == "forward"):
                fowardAdjust(42) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(42) #with parameter
        elif (quad == 7) or (quad == 13):
            return 58
            if (winch == "forward"):
                fowardAdjust(58) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(58) #with parameter
        elif (quad == 8) or (quad == 12):
            return 74
            if (winch == "forward"):
                fowardAdjust(74) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(74) #with parameter
        elif ((quad == 10) or (quad == 9) or (quad == 11)):
            return 90
            if (winch == "forward"):
                fowardAdjust(90) #with parameter for sail angle
            if (winch == "aft"):
                aftAdjust(90) #with parameter



#testing rudder
#start1 = time.perf_counter()
t1 = testing
#t1.testRudder()
#finish1 = time.perf_counter()
#print ("Finished in " + str((finish1 - start1)))


#testing navigation
#t1.testNavigation(27,-89)

#testing getHeading
test22 = (41.49008, -71.312796)
test23 = (41.499498, -81.695391)
print (Navigation.getHeading(test22,test23))

#GUI Testing
root = Tk()
root.geometry("500x700")
GUI = testingGUI(root)
root.mainloop()

