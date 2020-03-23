
import timeit
import time
import rudder
import datetime
import Nav
def cumNigger():
    start = start = time.time()
    jimbo = rudder.Rudder.Steer(270,360)
    print (jimbo)
    print ('{0:.8f} seconds elapsed.'.format(time.time()-start))


#cumNigger()

print (Nav.Navigation.wayPointReached())
