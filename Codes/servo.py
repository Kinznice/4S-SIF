import RPi.GPIO as GPIO
import serial
import time
import os
import base64
from datetime import datetime

servoPIN = 17

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN,GPIO.OUT)
GPIO.output(servoPIN,True)

pwm = GPIO.PWM(servoPIN,50)

pwm.start(2)

while True:
    pwm.ChangeDutyCycle(2)
    time.sleep(4)
    pwm.ChangeDutyCycle(4)
    time.sleep(0.8)
    pwm.ChangeDutyCycle(6)
    time.sleep(0.8)
    pwm.ChangeDutyCycle(8)
    time.sleep(0.8)
    pwm.ChangeDutyCycle(10)
    time.sleep(0.8)
    pwm.ChangeDutyCycle(12)
    time.sleep(0.8)
    