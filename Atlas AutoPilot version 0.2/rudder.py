class Rudder:
    def __init__(self, rudderAngle):
        #this is the variable that will be updated and passed into the methods to actually move the method: object name rudderMain
        self.rudderAngle = rudderAngle
    #rudderRange = [-45,45] -45 means to turn left, +45 is right turn

    #THIS NEEDS TO BE FIXED AND UPDATED
    def Steer(heading, tgtHeading):
        if (heading != tgtHeading):

            binHeading = Rudder.degreeToBin(heading)
            binTGTHeading = Rudder.degreeToBin(tgtHeading)
            #this divides up the results
            if (binHeading < binTGTHeading): #checks if a right turn is nessecary
                #checks directions of lowest turn

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
