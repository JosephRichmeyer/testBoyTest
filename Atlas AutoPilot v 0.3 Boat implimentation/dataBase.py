import sqlite3
from sqlite3 import Error
import datetime
import craftInfo
import Nav

class dataBase:

    #is it nessecary to use differnt or close cursors in any of these operations?
    def connectDB():
        try:
            global conn 
            conn = sqlite3.connect('AtlasLog.db')
            print("Connected to database AtlasLog.db")
        except:
            print("Unable to connect to database.")

    def createCursor():
        global curs 
        curs = conn.cursor()

        #creates tables at startup if not exist
    def createTable():
        try:
            curs.execute('''CREATE TABLE IF NOT EXISTS NavLog
            (DateTime text, CraftID int, Latitude real, Longitude real, Speed real, Heading, TargetHeading, ForWinch, AftWinch, RudderAngle, Tacking)  ''')
            conn.commit()
        except Error as e:
            print (e)

            #FYI boolean has to be numeric of 0 or 1
        try:
            curs.execute('''CREATE TABLE IF NOT EXISTS Waypoint (Number int, Latitude real, Longitude real, TackRange real, ReachDst real, Completed boolean)''')
            conn.commit()
        except Error as t:
            print(t)

    def insertWaypoint(Number, Latitude, Longitude, TackRange, ReachDst, Completed):
        try:
            wp = ("INSERT INTO Waypoint (Number, Latitude, Longitude, TackRange, ReachDst, Completed) VALUES ({}, {}, {}, {}, {}, {})".format(Number, Latitude, Longitude, TackRange, ReachDst, Completed))
            curs.execute(wp)
            conn.commit()
        except Error as r:
            print (r)
            print("Waypoint not added.")

    def updateWaypoint(pointNum, Latitude, Longitude, TackRange, ReachDst, Completed):
        try:
            uP = ("UPDATE Waypoint SET Latitude={},Longitude={},TackRange={},ReachDst={},Completed={} WHERE Number={}".format(Latitude,Longitude,TackRange,ReachDst,Completed,pointNum))
            curs.execute(wp)
            conn.commit()
        except Error as n:
            print(n)
            print("Failed to update Waypoint")

    def getCurrentWaypoint():
        try:
            cWP =("SELECT Number, Latitude, Longitude, TackRange, ReachDst, Completed FROM Waypoint WHERE Number = (Select min(Number) FROM WAYPOINT WHERE Completed = 0)")
            cock = curs.execute(cWP)
            cunt = curs.fetchone()
            #print (cunt)
            return cunt
        except Error as c:
            print (c)
            print ("Unable to get current waypoint.")

    #call this to complete current waypoint
    #this updates current waypoint Completed to "1"
    def completeCurrentWaypoint():
        try:
            curs.execute("UPDATE Waypoint SET Completed = 1 WHERE Number = (Select min(Number) FROM WAYPOINT WHERE Completed = 0) ")
            conn.commit()
        except Error as e:
            print(e)
            print("Failed to complete waypoint.")

    def getTackRange():
        try :
            tr = ("SELECT TackRange FROM Waypoint WHERE Number = (Select min(Number) FROM WAYPOINT WHERE Completed = 0)")
            tr1 = curs.execute(tr)
            tr2 = curs.fetchone()
            tr3 = tr2[0]
            print (tr3)
            return tr3
        except Error as e:
            print (e)
            print ("Failed to get tacking range")


    #def NavLogUpdate():
    #    try:
    #        np = ("INSERT INTO NavLog (DateTime, CraftID, Latitude, Longitude, Speed, Heading, TargetHeading, ForWinch, AftWinch, RudderAngle, Tacking) VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})".format(
    #            datetime.datetime.now(), craftInfo.craftID,  ))
         




