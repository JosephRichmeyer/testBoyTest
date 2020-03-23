import time
import craftInfo


class Rudder:
    def __init__(self):
        self.rudderAngle = rudderAngle

        #this is the variable that will be updated and passed into the methods to actually move the method: object name rudderMain
    rudderAngle = 0
    #rudderRange = [-45,45] -45 means to turn left, +45 is right turn

    #THIS NEEDS TO BE FIXED AND UPDATED
    def Steer():
        while True:
            print ("Running Steer 1")
            heading = craftInfo.craftInfo.heading
            tgtHeading = craftInfo.craftInfo.tgtHeading
            if (heading != tgtHeading):
                binHeading = Rudder.degreeToBin(heading) #removed Rudder.
                binTGTHeading = Rudder.degreeToBin(tgtHeading) #removed Rudder.
            
                #below is the attempted correction for the compass heading problem
                #checks to see if the -180,180 difference between heading and target heading is less than 0-360 and calculates turn accordingly
                if((heading - tgtHeading) <= (abs(binHeading) - abs(binTGTHeading))):
            
                    if (binHeading < binTGTHeading): #checks if a right turn is nessecary
                        #checks directions of lowest turn

                        Rudder.rudderAngle = Rudder.rudderMinMax(binTGTHeading - binHeading)
                        return Rudder.rudderAngle
                    else: #executes a left turn
                        Rudder.rudderAngle = Rudder.rudderMinMax(-(binHeading- binTGTHeading))
                        return Rudder.rudderAngle
                
                elif((heading - tgtHeading) > (abs(binHeading) - abs(binTGTHeading))):
                    if (heading < tgtHeading): #checks if a right turn is nessecary
                        #checks directions of lowest turn
                        Rudder.rudderAngle = Rudder.rudderMinMax(tgtHeading - heading)
                        return Rudder.rudderAngle
                    else: #executes a left turn
                        Rudder.rudderAngle = Rudder.rudderMinMax(-(heading- tgtHeading))
                        return Rudder.rudderAngle
                print (Rudder.rudderAngle)
                time.sleep(1)

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
#Rudder.Steer()