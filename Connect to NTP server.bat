net start w32time
w32tm /config /manualpeerlist:kinect-server,0x8 /syncfromflags:MANUAL /reliable:YES /update
sc config w32time start=auto
net start w32time
w32tm /query /status
pause