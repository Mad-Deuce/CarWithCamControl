#!/usr/bin/python3

#Серверная часть

import threading
import RPi.GPIO as GPIO     #импорт библиотеки для работы с GPIO
#import keyboard     #импорт библиотеки для работы с клавой
import time                 #импорт библиотеки для ожидания
from array import *         #импорт библиотеки для массивов
from threading import Thread

#import cv2 as cv

import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.1.237', 8089))
serversocket.listen(1) # become a server socket, maximum 5 connections


GPIO.cleanup()

GPIO.setmode(GPIO.BOARD)   #"запуск" GPIO

FRF=29              #переднее правое "вперед" (Front-Right-Forward)
FRB=31              #переднее правое "назад" (Front-Right-Backward)

FLF=35              #переднее левое "вперед" (Front-Left-Forward)
FLB=33              #переднее левое "назад" (Front-Left-Backward)

RRF=32              #заднее правое "вперед" (Rear-Right-Forward)
RRB=37              #заднее правое "назад" (Rear-Right-Backward)

RLF=36              #заднее левое "вперед" (Rear-Left-Forward)
RLB=38              #заднее левое "назад" (Rear-Left-Backward)

GPIO.setup(FRF, GPIO.OUT)    #объявление порта как выход-переднее правое
GPIO.setup(FRB, GPIO.OUT)    #объявление порта как выход-переднее правое

GPIO.setup(FLF, GPIO.OUT)    #объявление порта как выход-переднее правое
GPIO.setup(FLB, GPIO.OUT)    #объявление порта как выход-переднее правое

GPIO.setup(RRF, GPIO.OUT)    #объявление порта как выход-переднее правое
GPIO.setup(RRB, GPIO.OUT)    #объявление порта как выход-переднее правое

GPIO.setup(RLF, GPIO.OUT)    #объявление порта как выход-переднее правое
GPIO.setup(RLB, GPIO.OUT)    #объявление порта как выход-переднее правое 
########################################################################## 
# >>> bin(88) '0b1011000' >>> int('0b1011000', 2) 88 
# >>> >>> a=int('01100000', 2) >>> b=int('00100110', 2) >>> bin(a & b) '0b100000' 
# >>> bin(a | b) '0b1100110' >>> bin(a ^ b) '0b1000110' 
lock = threading.Lock()

TRMSi=3
TRMS=array('i',[int('00000000',2),
                int('11110000',2),
                int('00001111',2),
                int('11111111',2),
                int('00110011',2),
                int('11001100',2)
                ])
speedFi=0                                           #
SpeedWPM=0
SpeedT=array('i',[  int('00000000',2),
                    int('00000001',2),
                    int('00000011',2),
                    int('00000111',2),
                    int('00001111',2),
                    int('00011111',2),
                    int('00111111',2),
                    int('01111111',2),
                    int('11111111',2)
                    ])
speedF=array('f',[0.5,0.35,0.2,0.1,0.00])     #переменная скорости ВПЕРЕД
speedB=speedF[1]                                    #переменная скорости НАЗАД
speedLR=speedF[0]                                   #переменная скорости поворотов


########################################################################## 
def SpeedTakt():
    global SpeedWPM
    while True:
        # SpeedT=array('i',[  int('00000000',2),
        #                     int('00000001',2),
        #                     int('00000011',2),
        #                     int('00000111',2),
        #                     int('00001111',2),
        #                     int('00011111',2),
        #                     int('00111111',2),
        #                     int('01111111',2),
        #                     int('11111111',2)
        #                     ])
        for i in range (8):
            # lock.acquire()
            SpeedWPM=(SpeedT[speedFi]>>i) & 0b00000001
            # lock.release()
            #print('WPM-')
            #print(SpeedWPM)
            #time.sleep(0.001)
##########################################################################
th = Thread(target=SpeedTakt, daemon=True)
th.start()
##########################################################################  
def CarForward():
    defMask=0b01010101
    defMask=defMask & TRMS[TRMSi]

    gpioout7=((defMask & 0b10000000)>>7) & SpeedWPM
    gpioout6=((defMask & 0b01000000)>>6) & SpeedWPM
    gpioout5=((defMask & 0b00100000)>>5) & SpeedWPM
    gpioout4=((defMask & 0b00010000)>>4) & SpeedWPM
    gpioout3=((defMask & 0b00001000)>>3) & SpeedWPM
    gpioout2=((defMask & 0b00000100)>>2) & SpeedWPM
    gpioout1=((defMask & 0b00000010)>>1) & SpeedWPM
    gpioout0=((defMask & 0b00000001)>>0) & SpeedWPM

    GPIO.output(FRF, gpioout7)
    GPIO.output(FRB, gpioout6 )

    GPIO.output(FLF, gpioout5)
    GPIO.output(FLB, gpioout4)
    
    GPIO.output(RRF, gpioout3)
    GPIO.output(RRB, gpioout2)
    
    GPIO.output(RLF, gpioout1)
    GPIO.output(RLB, gpioout0)

    # GPIO.output(FRF, 0)
    # GPIO.output(FRB, 1)
    
    # GPIO.output(FLF, 0)
    # GPIO.output(FLB, 1)
    
    # GPIO.output(RRF, 0)
    # GPIO.output(RRB, 1)
    
    # GPIO.output(RLF, 0)
    # GPIO.output(RLB, 1)
    # if speedFi<4:
    #     CarStop()
    #     time.sleep(speedF[speedFi])
        
##########################################################################  
def CarBackward():
    defMask=0b10101010
    defMask=defMask & TRMS[TRMSi]

    gpioout7=(defMask & 0b10000000)>>7
    gpioout6=(defMask & 0b01000000)>>6
    gpioout5=(defMask & 0b00100000)>>5
    gpioout4=(defMask & 0b00010000)>>4
    gpioout3=(defMask & 0b00001000)>>3
    gpioout2=(defMask & 0b00000100)>>2
    gpioout1=(defMask & 0b00000010)>>1
    gpioout0=(defMask & 0b00000001)>>0

    GPIO.output(FRF, gpioout7)
    GPIO.output(FRB, gpioout6)
    
    GPIO.output(FLF, gpioout5)
    GPIO.output(FLB, gpioout4)
    
    GPIO.output(RRF, gpioout3)
    GPIO.output(RRB, gpioout2)
    
    GPIO.output(RLF, gpioout1)
    GPIO.output(RLB, gpioout0)

    # GPIO.output(FRF, 1)
    # GPIO.output(FRB, 0)
    
    # GPIO.output(FLF, 1)
    # GPIO.output(FLB, 0)
    
    # GPIO.output(RRF, 1)
    # GPIO.output(RRB, 0)
    
    # GPIO.output(RLF, 1)
    # GPIO.output(RLB, 0)
    # time.sleep(speedB)
##########################################################################
def CarLeft():
    defMask=0b01100110
    if TRMSi==1:
        defMask=defMask & TRMS[TRMSi+3]
    elif TRMSi==2:
        defMask=defMask & TRMS[TRMSi+3]
    else:
        defMask=defMask & TRMS[TRMSi]

    gpioout7=(defMask & 0b10000000)>>7
    gpioout6=(defMask & 0b01000000)>>6
    gpioout5=(defMask & 0b00100000)>>5
    gpioout4=(defMask & 0b00010000)>>4
    gpioout3=(defMask & 0b00001000)>>3
    gpioout2=(defMask & 0b00000100)>>2
    gpioout1=(defMask & 0b00000010)>>1
    gpioout0=(defMask & 0b00000001)>>0

    GPIO.output(FRF, gpioout7)
    GPIO.output(FRB, gpioout6)
    
    GPIO.output(FLF, gpioout5)
    GPIO.output(FLB, gpioout4)
    
    GPIO.output(RRF, gpioout3)
    GPIO.output(RRB, gpioout2)
    
    GPIO.output(RLF, gpioout1)
    GPIO.output(RLB, gpioout0)

    # GPIO.output(FRF, 0)
    # GPIO.output(FRB, 1)
    
    # GPIO.output(FLF, 1)
    # GPIO.output(FLB, 0)
    
    # GPIO.output(RRF, 0)
    # GPIO.output(RRB, 1)
    
    # GPIO.output(RLF, 1)
    # GPIO.output(RLB, 0)
    # time.sleep(speedLR)
##########################################################################
def CarRight():
    defMask=0b10011001
    if TRMSi==1:
        defMask=defMask & TRMS[TRMSi+3]
    elif TRMSi==2:
        defMask=defMask & TRMS[TRMSi+3]
    else:
        defMask=defMask & TRMS[TRMSi]

    gpioout7=(defMask & 0b10000000)>>7
    gpioout6=(defMask & 0b01000000)>>6
    gpioout5=(defMask & 0b00100000)>>5
    gpioout4=(defMask & 0b00010000)>>4
    gpioout3=(defMask & 0b00001000)>>3
    gpioout2=(defMask & 0b00000100)>>2
    gpioout1=(defMask & 0b00000010)>>1
    gpioout0=(defMask & 0b00000001)>>0

    GPIO.output(FRF, gpioout7)
    GPIO.output(FRB, gpioout6)
    
    GPIO.output(FLF, gpioout5)
    GPIO.output(FLB, gpioout4)
    
    GPIO.output(RRF, gpioout3)
    GPIO.output(RRB, gpioout2)
    
    GPIO.output(RLF, gpioout1)
    GPIO.output(RLB, gpioout0)

    # GPIO.output(FRF, 1)
    # GPIO.output(FRB, 0)
    
    # GPIO.output(FLF, 0)
    # GPIO.output(FLB, 1)
    
    # GPIO.output(RRF, 1)
    # GPIO.output(RRB, 0)
    
    # GPIO.output(RLF, 0)
    # GPIO.output(RLB, 1)
    # time.sleep(speedLR)
##########################################################################
def CarStop(): 
    GPIO.output(FRF, 0)
    GPIO.output(FRB, 0)
    
    GPIO.output(FLF, 0)
    GPIO.output(FLB, 0)
    
    GPIO.output(RRF, 0)
    GPIO.output(RRB, 0)
    
    GPIO.output(RLF, 0)
    GPIO.output(RLB, 0)
########################################################################## 
# NON Working
def CarAction():
    controlSym=''
    while True:
        if controlSym=='w':
            defMask=0b01010101                  #Активные выхода для движения вперед
        elif controlSym=='s':
            defMask=0b10101010                  #Активные выхода для движения назад
        elif controlSym=='a':
            defMask=0b10101010                  #Активные выхода для движения назад
        elif controlSym=='d':
            defMask=0b10101010                  #Активные выхода для движения назад
        else:
            defMask=0b00000000                  #Активные выхода для движения назад
        
        defMask=defMask & TRMS[TRMSi]

        gpioout7=(defMask & 0b10000000)>>7
        gpioout6=(defMask & 0b01000000)>>6
        gpioout5=(defMask & 0b00100000)>>5
        gpioout4=(defMask & 0b00010000)>>4
        gpioout3=(defMask & 0b00001000)>>3
        gpioout2=(defMask & 0b00000100)>>2
        gpioout1=(defMask & 0b00000010)>>1
        gpioout0=(defMask & 0b00000001)>>0

        GPIO.output(FRF, gpioout7)
        GPIO.output(FRB, gpioout6)
        
        GPIO.output(FLF, gpioout5)
        GPIO.output(FLB, gpioout4)
        
        GPIO.output(RRF, gpioout3)
        GPIO.output(RRB, gpioout2)
        
        GPIO.output(RLF, gpioout1)
        GPIO.output(RLB, gpioout0)

########################################################################## 
while True:
    connection, address = serversocket.accept()

    while True:
        buf = connection.recv(64)
        #time.sleep(1)
        if len(buf) > 0:
            if buf.decode('utf-8') == 'w':
                CarForward()
            elif buf.decode('utf-8') == 's':
                CarBackward()
            elif buf.decode('utf-8') == 'a':         
                CarLeft()
            elif buf.decode('utf-8') == 'd':
                CarRight()
            elif buf.decode('utf-8') == 'stopthecar':
                CarStop()
            elif buf.decode('utf-8') == 'disconnect':
                CarStop()
                break
            elif buf.decode('utf-8') == 'r':
                if speedFi<8:
                    speedFi=speedFi+1
                    print(speedFi)
            elif buf.decode('utf-8') == 'f':
                if speedFi>0:
                    speedFi=speedFi-1
                    print(speedFi)
            elif buf.decode('utf-8') == 'z':
                TRMSi=0
                print(TRMSi)
            elif buf.decode('utf-8') == 'x':
                TRMSi=1
                print(TRMSi)
            elif buf.decode('utf-8') == 'c':
                TRMSi=2
                print(TRMSi)
            elif buf.decode('utf-8') == 'v':
                TRMSi=3
                print(TRMSi)
            else:
                CarStop()        
        else:
            CarStop()