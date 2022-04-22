#!/usr/bin/python3

#Серверная часть

import RPi.GPIO as GPIO     #импорт библиотеки для работы с GPIO
#import keyboard     #импорт библиотеки для работы с клавой
import time                 #импорт библиотеки для ожидания

import cv2 as cv

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

GPIO.setup(FRF, GPIO.OUT)    #объявление порта 3 как выход-переднее правое
GPIO.setup(FRB, GPIO.OUT)    #объявление порта 5 как выход-переднее правое

GPIO.setup(FLF, GPIO.OUT)    #объявление порта 3 как выход-переднее правое
GPIO.setup(FLB, GPIO.OUT)    #объявление порта 5 как выход-переднее правое

GPIO.setup(RRF, GPIO.OUT)    #объявление порта 3 как выход-переднее правое
GPIO.setup(RRB, GPIO.OUT)    #объявление порта 5 как выход-переднее правое

GPIO.setup(RLF, GPIO.OUT)    #объявление порта 3 как выход-переднее правое
GPIO.setup(RLB, GPIO.OUT)    #объявление порта 5 как выход-переднее правое 
 
########################################################################## 
def CarForward():
    GPIO.output(FRF, 0)
    GPIO.output(FRB, 1)
    
    GPIO.output(FLF, 0)
    GPIO.output(FLB, 1)
    
    GPIO.output(RRF, 0)
    GPIO.output(RRB, 1)
    
    GPIO.output(RLF, 0)
    GPIO.output(RLB, 1)
##########################################################################  
def CarBackward():
    GPIO.output(FRF, 1)
    GPIO.output(FRB, 0)
    
    GPIO.output(FLF, 1)
    GPIO.output(FLB, 0)
    
    GPIO.output(RRF, 1)
    GPIO.output(RRB, 0)
    
    GPIO.output(RLF, 1)
    GPIO.output(RLB, 0)
##########################################################################
def CarLeft():
    GPIO.output(FRF, 0)
    GPIO.output(FRB, 1)
    
    GPIO.output(FLF, 1)
    GPIO.output(FLB, 0)
    
    GPIO.output(RRF, 0)
    GPIO.output(RRB, 1)
    
    GPIO.output(RLF, 1)
    GPIO.output(RLB, 0)
##########################################################################
def CarRight():
    GPIO.output(FRF, 1)
    GPIO.output(FRB, 0)
    
    GPIO.output(FLF, 0)
    GPIO.output(FLB, 1)
    
    GPIO.output(RRF, 1)
    GPIO.output(RRB, 0)
    
    GPIO.output(RLF, 0)
    GPIO.output(RLB, 1)
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
#capture = cv.VideoCapture(0)

#while(True):
#    ret, frame = capture.read()
#    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
#    size=(160,120)
#    out = cv.resize(gray,size)

    #cv.imshow('frame',gray)
    #cv.imshow('frame',frame)
#    cv.imshow('frame',out)
#    if cv.waitKey(1) & 0xFF == ord('q'):
#        break
#capture.release()
#cv.destroyAllWindows()

########################################################################## 
while True:
    connection, address = serversocket.accept()
    capture = cv.VideoCapture(0)

    while True:
        buf = connection.recv(64)

        ret, frame = capture.read()
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        size=(160,120)
        out = cv.resize(gray,size)
        
        midata = out.read(1024)
        while midata:
            connection.send(out)
            midata = out.read(1024)
            
            #sock.sendto(midata, addr)
            #midata = mifile.read(1024)

        #connection.send(out)

        #print(buf)
        #print('.')
        #time.sleep(1)
        if len(buf) > 0:
            #print(buf.decode('utf-8'))
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
            else:
                CarStop()        
        else:
            CarStop()