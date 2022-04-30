#!/usr/bin/python3

#Серверная часть

import threading
import RPi.GPIO as GPIO     #импорт библиотеки для работы с GPIO
#import keyboard     #импорт библиотеки для работы с клавой
import time                 #импорт библиотеки для ожидания
from array import *         #импорт библиотеки для массивов
from threading import Thread

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

PWM=12              #выход ШИМ

GPIO.setup(FRF, GPIO.OUT)           #объявление порта как выход
GPIO.setup(FRB, GPIO.OUT)           #объявление порта как выход

GPIO.setup(FLF, GPIO.OUT)           #объявление порта как выход
GPIO.setup(FLB, GPIO.OUT)           #объявление порта как выход

GPIO.setup(RRF, GPIO.OUT)           #объявление порта как выход
GPIO.setup(RRB, GPIO.OUT)           #объявление порта как выход

GPIO.setup(RLF, GPIO.OUT)           #объявление порта как выход
GPIO.setup(RLB, GPIO.OUT)           #объявление порта как выход

GPIO.setup(PWM, GPIO.OUT)           #объявление порта как выход

pwmOutput_0 = GPIO.PWM(PWM, 100)    #Создаем объект pwmOutput_0 для работы с каналами PWM
########################################################################## 
 
# lock = threading.Lock()

TRMSi=3
TRMS=array('i',[int('00000000',2),
                int('11110000',2),
                int('00001111',2),
                int('11111111',2),
                int('00110011',2),
                int('11001100',2)
                ])
speedPWMi=0               #
speedPWM=array('i',[30,40,50,75,100])     #переменная скорости ВПЕРЕД

pwmi=-1
pwmduty=30
########################################################################## 
def SpeedTakt():
    global pwmduty
    global pwmi
    while True:
        if pwmduty<31:
            pwmduty=30
        elif pwmduty>99:
            pwmduty=99

        pwmduty=pwmduty+1*(pwmi)    
        time.sleep(0.1)
        print(pwmduty)
##########################################################################
th = Thread(target=SpeedTakt, daemon=True)
th.start()
##########################################################################  
def CarForward():
    
    pwmOutput_0.start(pwmduty)

    defMask=0b01010101
    defMask=defMask & TRMS[TRMSi]

    gpioout7=((defMask & 0b10000000)>>7)
    gpioout6=((defMask & 0b01000000)>>6)
    gpioout5=((defMask & 0b00100000)>>5)
    gpioout4=((defMask & 0b00010000)>>4)
    gpioout3=((defMask & 0b00001000)>>3)
    gpioout2=((defMask & 0b00000100)>>2)
    gpioout1=((defMask & 0b00000010)>>1)
    gpioout0=((defMask & 0b00000001)>>0)

    GPIO.output(FRF, gpioout7)
    GPIO.output(FRB, gpioout6 )

    GPIO.output(FLF, gpioout5)
    GPIO.output(FLB, gpioout4)
    
    GPIO.output(RRF, gpioout3)
    GPIO.output(RRB, gpioout2)
    
    GPIO.output(RLF, gpioout1)
    GPIO.output(RLB, gpioout0)
       
##########################################################################  
def CarBackward():
    pwmOutput_0.start(speedPWM[2])

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

##########################################################################
def CarLeft():
    pwmOutput_0.start(pwmduty)

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

##########################################################################
def CarRight():
    pwmOutput_0.start(pwmduty)

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

##########################################################################
def CarStop(): 
    # pwmOutput_0.stop()

    GPIO.output(FRF, 0)
    GPIO.output(FRB, 0)
    
    GPIO.output(FLF, 0)
    GPIO.output(FLB, 0)
    
    GPIO.output(RRF, 0)
    GPIO.output(RRB, 0)
    
    GPIO.output(RLF, 0)
    GPIO.output(RLB, 0)
########################################################################## 

########################################################################## 
while True:
    connection, address = serversocket.accept()

    while True:
        buf = connection.recv(64)
        #time.sleep(1)
        if len(buf) > 0:
            if buf.decode('utf-8') == 'w':
                pwmi=1
                CarForward()
            elif buf.decode('utf-8') == 's':
                CarBackward()
            elif buf.decode('utf-8') == 'a':
                pwmi=1         
                CarLeft()
            elif buf.decode('utf-8') == 'd':
                pwmi=1
                CarRight()
            elif buf.decode('utf-8') == 'stopthecar':
                pwmi=-3
                CarStop()
            elif buf.decode('utf-8') == 'disconnect':
                pwmOutput_0.stop()
                CarStop()
                break
            elif buf.decode('utf-8') == 'r':
                if speedPWMi<4:
                    speedPWMi=speedPWMi+1
                    print(speedPWMi)
            elif buf.decode('utf-8') == 'f':
                if speedPWMi>0:
                    speedPWMi=speedPWMi-1
                    print(speedPWMi)
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
                pwmi=-3
                CarStop()        
        else:
            pwmi=-3
            CarStop()