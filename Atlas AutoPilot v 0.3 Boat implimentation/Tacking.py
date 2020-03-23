import dataBase
import sensors

#this class just holds the tacking algorithm
#this returns waypoints for the target
dataBase.dataBase.connectDB()
dataBase.dataBase.createCursor()
dataBase.dataBase.createTable()
print (dataBase.dataBase.getTackRange())
tack.createTackPoints()


#call create tacking waypoints once when tacking begins
#this creates a list of waypoints to tack to
#assuming tacking at 45 degrees always, 
class tack:
    tackAngle = 45 #degrees: this can change = B in triangle
    def createTackPoints():
        waypointList = []
        #gets current waypoint
        try:
            point = dataBase.dataBase.getCurrentWaypoint()
            lat = point[1]
            print (lat)
            long = point[2]
            print (long)
            tackRNG = point[3]
        except Error as e:
            print (e)
            print ("Failed to get current waypoint when setting tack points")

        #creating waypoint 1
        try:
            angleC = 90 #degrees
            angleA = 180 - (angleC + tackAngle)
            angleB = tackAngle
            sideA = tackRNG
            sideB = tackRNG
            sideC = squrt((sidA ** 2) + (sideB ** 2))
            crntLat = sensors.Sensors.getLong()
            crntLong = sensors.Sensors.getLat()
            print (crntLat)
            print (crntLong)
        #except:
        #    print ("somet")

        #target waypoint should be left 
        #make waypoint 1 in the direction of least wind
        #make waypoints with double triangle length so it crosses to next point on other side
        # then tack after hitting range off waypoints

        #Joseph, Add this all to the py and run it there

