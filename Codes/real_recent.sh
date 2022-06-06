#!/bin/bash
# lcd > file directory in Pi
# cd > file directory in computer
# ID > ID for FTP, PW > password for FTP

DATE=$(date +"%Y_%m_%d_%H_%M_%S")

raspistill -o /home/pi/camera/real/$DATE-TNF-PHENO.jpg -r -rot 180

ftp -v -n<<!
open 147.46.229.129
user ID PW
bi
cd pheno/
lcd camera/real 
prompt
mput *.jpg
bye
!

find /home/pi/camera/real -name "*.jpg" -exec rm -rf {} \;

