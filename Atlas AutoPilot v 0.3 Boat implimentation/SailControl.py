import time

class sailControl:
    def __init__(self, aftWinch, forwardWinch):
        self.aftWinch = aftWinch
        self.forwardWinch = forwardWinch

    def sailAdjust(winch):
        #adjusts winches to paramenter angle (or quadrant)
        try:
            quad = sensors.Sensors.getWindQuad()
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