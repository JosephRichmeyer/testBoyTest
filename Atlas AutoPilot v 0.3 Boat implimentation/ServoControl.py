
#import RPi.GPIO as GPIO

#initializing servo
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(12, GPIO.OUT)
#p = GPIO.PWM(12, 50)
#p.start(7.5)

#class servoControl:

#    def servoSail(ang):
#        if (ang == 0):
#            p.ChangeDutyCycle(7.5)
#        elif (ang < 0):
#            p.ChangeDutyCycle( 7.5+(2.5*(abs(ang)/45)))
#        elif (ang > 0):
#            p.ChangeDutyCycle( 7.5-(2.5*(abs(ang)/45)))