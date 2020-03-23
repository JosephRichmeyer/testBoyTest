
import random
import time
import math
from collections import Counter
import ThreadWorker
import Nav
import SailControl
#import sensors
import rudder
import dataBase
import Tacking



#Creating single objects for each class
#rudderMain = rudder.Rudder(0)
#sailMain = SailControl.sailControl(0,0) # aft is first forward is second
#sensor = sensors.Sensors(0, 0, 0)



#if __name__ == "__main__":

#    sailMain = SailControl.sailControl(0,0) # aft is first forward is second
#    sensor = sensors.Sensors(0, 0, 0)
#    print ("Atlas Autopilot version 0.3")
#    try:
#        dataBase.dataBase.connectDB()
#        dataBase.dataBase.createCursor()
#        dataBase.dataBase.createTable()
#        print("Successfully connected to database.")
#    except:
#        print ("Failed to connect to database at startup.")
#    try:
#        print (dataBase.dataBase.getTackRange())
#    except:
#        print ("Failed to start threading.")



#class jobTimer:
#rudder.Rudder.Steer() runs every .2 seconds
#Nav.Navigation.wayPointReached() runs every 15 seconds

#windLogger runs once per second
#sailAdjuster runs every 60 seconds
#calls sailAdjust

#NavLog gets updated every second but make sure to remember to check if "craftinfo.active = false"
#sample threading function for Navlog




class actionThreading:
    def threadStart():
        print ("Threads Started")
        threading.Thread(target=startSteer).start()
    def startSteer():
        print("Rudder Steering Initialized")
        while True:
            rudderMain.Steer()#get current heading, target heading)
            time.sleep(.1)

    def updateGPS():
        #gets gps data and updates the current craft heading
        return True



