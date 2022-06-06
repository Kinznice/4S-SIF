import spidev
import time
import sched
import os 
import serial
import numpy as np
import re
import sys

# Time interval
interval = 1
# Sleep for RCT module
time.sleep(60)
# Start time
sTime = time.strftime('%Y_%m_%d_%H_%M_%S',time.localtime(time.time()))

# Saving location
url1='/home/pi/RAW/FS_RAW_UP_%s.txt' % (sTime)
url2='/home/pi/SIF/FS_SIF_%s.txt' % (sTime)

t0 = time.localtime(time.time())        
        
while True:
    t = time.localtime(time.time())
    #if (t.tm_sec==0 or t.tm_sec==2 or t.tm_sec==4 or t.tm_sec==6 or t.tm_sec==8 or t.tm_sec==10 or t.tm_sec==12 or t.tm_sec==14 or t.tm_sec==16 or t.tm_sec==18 or t.tm_sec==20 or t.tm_sec==22 or t.tm_sec==24 or t.tm_sec==26 or t.tm_sec==28 or t.tm_sec==30 or t.tm_sec==32 or t.tm_sec==34 or t.tm_sec==36 or t.tm_sec==38 or t.tm_sec==40 or t.tm_sec==42 or t.tm_sec==44 or t.tm_sec==46 or t.tm_sec==48 or t.tm_sec==50 or t.tm_sec==52 or t.tm_sec==54 or t.tm_sec==56 or t.tm_sec==58):
    if (t.tm_sec>=0) :
  
        ser = serial.Serial('/dev/ttyUSB0', 57600, timeout = 1)
        ser.close()
        ser.open()

        com1 = "#RS2\n"
        com2 = "#RS1\n" 
        
        time.sleep(0.2)
        ser.write(bytes(com1.encode()))
        time.sleep(0.2)
        dresponse1 = ser.readline()
        
        dstr1=str(dresponse1)
        dstr2=','
        dstr3="'"
        dstr4='n'
        dlag2=[m.start () for m in re.finditer(dstr2, dstr1)]
        #print(dresponse1)
        #print(dlag2)
        if not dlag2:
            print('Upward Sensor is disconnected')
            #os.system('sudo reboot')
        dlag3=[m.start () for m in re.finditer(dstr3, dstr1)]
        dlag4=[m.start () for m in re.finditer(dstr4, dstr1)]
        #dtemp1=dlag3[0]+1
        #dtemp2=dlag2[0]+1
        #dtemp3=dlag3[0]-1

        da75=dstr1[dlag2[1]+1:dlag2[2]]
        da76=dstr1[dlag2[2]+1:dlag2[3]]
        da77=dstr1[dlag2[3]+1:dlag4[0]-1]
        #print(da75,da76,da77)
        
        time.sleep(0.2)
        ser.write(bytes(com1.encode()))
        time.sleep(0.2)
        uresponse1 = ser.readline()
        
        ustr1=str(uresponse1)
        ustr2=','
        ustr3="'"
        ustr4='n'
        ulag2=[m.start () for m in re.finditer(ustr2, ustr1)]
        if not ulag2:
            print('Upward Sensor is disconnected')
            #os.system('sudo reboot')
        ulag3=[m.start () for m in re.finditer(ustr3, ustr1)]
        ulag4=[m.start () for m in re.finditer(ustr4, ustr1)]

        ua75=ustr1[ulag2[1]+1:ulag2[2]]
        ua76=ustr1[ulag2[2]+1:ulag2[3]]
        ua77=ustr1[ulag2[3]+1:ulag4[0]-1]
        #print(ua75,ua76,ua77)

        darr1=np.array(da75,np.float)
        darr2=np.array(da76,np.float)
        darr3=np.array(da77,np.float)

        D75=np.mean(darr1)
        D76=np.mean(darr2)
        D77=np.mean(darr3)
        
        uarr1=np.array(ua75,np.float)
        uarr2=np.array(ua76,np.float)
        uarr3=np.array(ua77,np.float)

        U75=np.mean(uarr1)
        U76=np.mean(uarr2)
        U77=np.mean(uarr3)
        
        file1=open(url1,'a')
        #file1.write('%s, w756: %10.2f, w760: %10.2f, w770: %10.2f\n' % (time.strftime('%Y-%m-%d %H:%M:%S',t), date756, date760, date770))
        print('%s, U75: %s, U76: %s, U77: %s, U75: %s, U76: %s, U77: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S',t), U75, U76, U77, D75, D76, D77))
        file1.write('%s, U75: %s, U76: %s, U77: %s, U75: %s, U76: %s, U77: %s\n' % (time.strftime('%Y-%m-%d %H:%M:%S',t), U75, U76, U77, D75, D76, D77))
        file1.close()
    
        t0 = t
        time.sleep(0.2)
        
s = sched.scheduler(time.time, time.sleep)

# Set start time
timestamp = time.mktime(time.strptime(sTime,'%Y_%m_%d_%H_%M_%S'))

# Start
s.enterabs(timestamp, 1, do, ())
s.run()

    
  
