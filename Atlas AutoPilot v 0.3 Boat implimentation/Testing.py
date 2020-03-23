import requests
import sensors
import ServoControl
import SailControl
import Nav
import rudder
import json
import tkinter as tk
from tkinter import *


#BELOW IS ALL FOR DEMONSTRATION TESTING
class testing:
    #methods below
    def testRudder():
        for i in range(20):
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
    #nd an input as current craft heading
    #using location, gets the wind direction from openmaps
    #then prints the target heading, wind direction and speed at the location,
    def __init__(self, master):
        self.master = master
        master.title("Atlas Autopilot GUI Tester")
        self.label = Label(master, text="This is a snapshot of the Atlas autpilot functions based upon sensor inputs.")
        self.label.pack()
        self.label2 = Label(master, text="Instead of anemometer input, real weather data is downloaded from OpenWeather.")
        self.label2.pack()

        self.CLButton = Button(master, text="Use Current Location", command=fillCurrentGPS)
        self.CLButton.pack()

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

        self.targetHead = Text(master, height=1,width=10)
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
        nav1 = Nav.Navigation.getHeading(dst1,dst2)
        #deletes fields
        self.distance.delete('1.0', END)
        self.targetHead.delete('1.0', END)
        self.windSpeedtxt.delete('1.0', END)
        self.windHead.delete('1.0',END)
        self.sailAng.delete('1.0',END)
        self.rudderAngle.delete('1.0', END)

        #updates fields
        self.distance.insert(INSERT, Nav.Navigation.getDistance(dst1,dst2))
        self.targetHead.insert(INSERT, str(nav1))
        self.windHead.insert(INSERT, testing.testNavigation(lat1,long1,"direction"))
        self.windSpeedtxt.insert(INSERT, (2.23694 * (testing.testNavigation(lat1,long1,"speed"))))
        windHeadBin = rudder.Rudder.degreeToBin(testing.testNavigation(lat1,long1,"direction"))
        tgtHeadBin = rudder.Rudder.degreeToBin(float(nav1))
        self.sailAng.insert(INSERT, testingGUI.windTestQuad(sensors.Sensors.toQuadrant(abs(tgtHeadBin-windHeadBin))))

        correction = rudder.Rudder.degreeToBin(float(nav1)) - rudder.Rudder.degreeToBin(float(head1))
        self.rudderAngle.insert(INSERT, rudder.Rudder.rudderMinMax(correction))
        servoControl.servoSail(rudder.Rudder.rudderMinMax(correction))

    def windTestQuad(quad):
        if ((quad == 1) or (quad == 2) or (quad == 3) or (quad == 17) or (quad == 18)):
            print ("Wind insufficent, tacking needed:")
            Nav.Navigation.tack()
            return "Tacking"
            tack() #create tacking algorithm with tack distance
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



##testing rudder
#start1 = time.perf_counter()
#t1 = testing
#t1.testRudder()
#finish1 = time.perf_counter()
#print ("Finished in " + str((finish1 - start1)))


#testing navigation
#t1.testNavigation(27,-89)

#testing getHeading
#test22 = (41.49008, -71.312796)
#test23 = (41.499498, -81.695391)
#print (Navigation.getHeading(test22,test23))

##this fills current location in the gui with current location from gps module
##the problem is that it defines the object but these dont integrate with the object
#def fillCurrentGPS():
#    print (sensors.Sensors.getLat())
#    GUI.lat_entry.insert(0, sensors.Sensors.getLat())
#    GUI.lat_entry.pack()
#    GUI.long_entry.insert(0, sensors.Sensors.getLong())
#    GUI.long_entry.pack()
#    print ("Current GPS Filled")

##GUI Testing
#root = Tk()
#root.geometry("600x700")
#root['bg'] = '#BFF6FE'
#GUI = testingGUI(root)
#root.mainloop()