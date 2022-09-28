import RPi.GPIO as GPIO
import serial
import time
import os
import base64
from datetime import datetime

filters = {
    2:75,
    4:76,
    6:77,
    8:00,
    10:11,
    12:12
}
#time.sleep(60)
servoPIN = 18

sTime = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))
#print(sTime)
# File URL
url = '/home/pi/4S_SIF_v1/FS_SIF_DC_%s.txt' % (sTime)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN,GPIO.OUT)

pwm = GPIO.PWM(servoPIN,50)
pwm.start(2)

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
            log = str(timeTaken)  + "," + str(filters[pos]) + "," + str(voltage ) + "," + "rw:" + "," + (pp[0][3:7]) + "," + (pp[1][0:4] ) + "," +  str(int(pp[0][3:7],16)) + "," +  str(int(pp[1][0:4],16))     
            
            print(log )
                        
            with open(url,"a") as f:
                f.write(log + "\n")
                
            #time.sleep(0.048)
                
            cntTime = time.perf_counter()           
        
        
        if pos == 8 :
            pos  = 2
            k = 2.4
            
        else:
            pos = pos + 2
            if pos == 4 :
                k = 4.4
            elif pos == 6 :
                k = 6.6
            elif pos == 8 :
                k = 8.8
        
    except:
        print(cc)
        print('Serial Communication Error')
        
        
pwm.stop()
GPIO.cleanup()
        

    
    
