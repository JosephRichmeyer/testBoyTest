from threading import Thread
import time
import rudder
import SailControl
import sensors
  



def runA():
    while True:
        print("Ran A Sleep 3")
        time.sleep(3)

def runB():
    while True:
        print("Ran B Sleep 5")
        time.sleep(5)

def runC():
    while True:
        print("Ran C Sleep 10")
        time.sleep(10)


while True:
    t1 = Thread(target = sensors.Sensors.windLogger)

    t1.setDaemon(True)

    t1.start()

    while True:
        pass
