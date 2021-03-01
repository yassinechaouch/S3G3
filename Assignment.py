 import RPi.GPIO as GPIO

 GPIO.setwarnings(false)
 GPIO.setmode(GPIO.BOARD)
 sensor=8 
 led=10
 GPIO.setup(sensor,GPIO.IN)
 GPIO.setup(led, GPIO.OUT)
 while True :

    if GPIO.input(sensor):
        GPIO.output(led, GPIO.HIGH)
    else :
        GPIO.output(led, GPIO.LOW)
