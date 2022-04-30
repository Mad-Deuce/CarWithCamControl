#!/usr/bin/python3

#клиентская часть

from doctest import testsource
import keyboard     #импорт библиотеки для работы с клавой
import socket
import time
import sys
import cv2 as cv
from threading import Thread
pwmi=-1
pwmduty=0
########################################################################## 
def SpeedTakt():
    global pwmduty
    global pwmi
    while True:
        if pwmduty<30:
            pwmduty=30
        elif pwmduty>99:
            pwmduty=99

        pwmduty=pwmduty+1*(pwmi)    
        time.sleep(0.2)
        print(pwmduty)
##########################################################################
th = Thread(target=SpeedTakt, daemon=True)
th.start()
##########################################################################
########################################################################## 
def test(x):
    global pwmi
    if x.event_type == 'down': 
        if x.name == 'w':  
            pwmi=1
    else:
            pwmi=-1
        # clientsocket.send(f'stopthecar'.encode('utf-8'))
        # print("fdfdfdf")
########################################################################## 

########################################################################## 

keyboard.hook(test)
keyboard.wait("p")
# clientsocket.close()
# break