## Import codes ## 

import RPi.GPIO as GPIO
import serial
import time
import os
import base64
from datetime import datetime
import Adafruit_DHT

## Set GPIO ##
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

## Set motor location for Filter numbers ##
filters = {
    2:75, ## For 755 nm filter
    4:76, ## For 760 nm filter
    6:77, ## For 770 nm filter
    8:00,
    10:11,
    12:12
}

SERVO_PIN = 18  ## Set servo motor GIO PIN
TEMP_PIN = 23  ## Set Temp/Humi sensor GIO PIN

DHT22 = Adafruit_DHT.AM2302 ## Set Temp/Humi sensor

sw_L  = 6 ## Setting for geared motor
sw_R  = 5 ## Setting for geared motor
pwmL = 13 ## Setting for geared motor
pwmR = 12 ## Setting for geared motor

## Set GPIO ##
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(sw_L,GPIO.IN)
GPIO.setup(sw_R,GPIO.IN)
GPIO.setup(pwmL,GPIO.OUT)
GPIO.setup(pwmR,GPIO.OUT)

##updown motor speed
dcspeed =50      

print("Warming Up ...")
for cnt in range(40):
    print(40-cnt ," ...")
    time.sleep(1)

## Saved file directory ##
sTime = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
#print(sTime)
# File URL
url = '/home/pi/4S_SIF_v2/FS_SIF_v2_%s.txt' % (sTime)

## Geard motor setting ##
pwm = GPIO.PWM(SERVO_PIN,50)
pwm.start(2)

pwm_L = GPIO.PWM(pwmL,100)
pwm_R  = GPIO.PWM(pwmR,100)

pwm_R.start(dcspeed)
pwm_L.start(dcspeed)

## Set Temp/Humi sensor ##
humidity,temperature = 0.0,0.0
updown = 0

extraTag = "Temp= {0:0.1f} C , Humi= {1:0.1f} % ".format(temperature, humidity)

## Setting for Photodiode ADC ##
ser = serial.Serial(
    port = '/dev/ttyUSB_P1',
    baudrate = 19200,
    timeout = 1,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_TWO,
    bytesize = serial.EIGHTBITS
)
    
line = []
cc = " "
pos = 2
k = 2.4
log = " "

fn = datetime.now().strftime("%Y%m%d-%H%M%S" + ".txt")
sday = datetime.now().day

##updown Motor Set Left
if GPIO.input(sw_L) == 0:
    pwm_R.ChangeDutyCycle(dcspeed)
    pwm_L.ChangeDutyCycle(0)
    time.sleep(2)
    

pwm_R.ChangeDutyCycle(0)
pwm_L.ChangeDutyCycle(dcspeed)
while GPIO.input(sw_L):
    time.sleep(0.05)
pwm_L.ChangeDutyCycle(0)


## Main body for data collection ##
time.sleep(10)
while True:
    today = datetime.now().day
    if sday != today:
       sday = today
       fn = datetime.now().strftime("%Y%m%d-%H%M%S" + ".txt") 
    try:        
        pwm.ChangeDutyCycle(k)
        if pos > 3:
            time.sleep(2)
            pwm.ChangeDutyCycle(0)
        else:
            time.sleep(2)
            pwm.ChangeDutyCycle(0)
            
        cntTime = time.perf_counter()
        cntTarget = cntTime + 1
        while cntTime  < cntTarget:
            
            cc = str(ser.readline())            
            pp= cc.split(',')
            
            timeTaken = datetime.fromtimestamp(time.time())            
            voltage = round(int(pp[0][3:7],16) * ( 5.0 / int(pp[1][0:4],16)),6)        
            
            ###      timeTaken              Filter             Voltage            Raw
            log = str(timeTaken)  + "," + str(filters[pos]) + "," + str(voltage ) + "," + "rw:" + "," + (pp[0][3:7]) + "," + (pp[1][0:4] ) + "," +  str(int(pp[0][3:7],16)) + "," +  str(int(pp[1][0:4],16)) + ", " + "Updown: " + str(updown) + "," +  extraTag
            
            print(log )
                        
            with open(url,"a") as f:
                f.write(log + "\n")
                
            #time.sleep(0.048)
                
            cntTime = time.perf_counter()           
        
        
        if pos == 8 :
            pos  = 2
            k = 2.4

            humidity, temperature = Adafruit_DHT.read_retry(DHT22,TEMP_PIN)
            if humidity is not None and temperature is not None:
                print("UpDown : ", updown, " Temp={0:0.1f} C Humidity={1:0.1f}%".format(temperature, humidity))
                if humidity < 100 :
                    extraTag = "Temp: {0:0.1f} C , Humi: {1:0.1f} %".format(temperature, humidity)
            else:
                print("Sensor failure, CHeck wiring. ")

            updown = ( updown + 1 ) % 2
            if updown == 0:
                pwm_R.ChangeDutyCycle(0)
                pwm_L.ChangeDutyCycle(dcspeed)
                while GPIO.input(sw_L):
                    time.sleep(0.05)
                pwm_L.ChangeDutyCycle(0)
            else:
                pwm_L.ChangeDutyCycle(0)
                pwm_R.ChangeDutyCycle(dcspeed)
                while GPIO.input(sw_R):
                    time.sleep(0.05)
                pwm_R.ChangeDutyCycle(0)  
            
            
        else:
            pos = pos + 2
            if pos == 4 :
                k = 4.4
            elif pos == 6 :
                k = 6.5
            elif pos == 8 :
                k = 8.5
        
    except:
        print(cc)
        print('Serial Communication Error')
        
        
pwm.stop()
GPIO.cleanup()

##        
##            ##temperature, upDown
##            humidity, temperature = Adafruit_DHT.read(DHT22,TEMP_PIN)
##            if humidity is not None and temperature is not None:
##                print("UpDown : ", updown, " Temp={0:0.1f} C Humidity={1:0.1f}%".format(temperature, humidity))
##                if humidity < 100.0 :
##                    extraTag = "Updown: {0} , Temp: {1:0.1f} C , Humi: {2:0.1f} %".format(updown,temperature, humidity)
##            else:
##                print("Sensor failure, CHeck wiring. ")
##
##            updown = ( updown + 1 ) % 2
##            if updown == 0:
##                pwm_R.ChangeDutyCycle(0)
##                pwm_L.ChangeDutyCycle(dcspeed)
##                while GPIO.input(sw_L):
##                    time.sleep(0.05)
##                pwm_L.ChangeDutyCycle(0)
##            else:
##                pwm_L.ChangeDutyCycle(0)
##                pwm_R.ChangeDutyCycle(dcspeed)
##                while GPIO.input(sw_R):
##                    time.sleep(0.05)
##                pwm_R.ChangeDutyCycle(0)  
        

    
    
