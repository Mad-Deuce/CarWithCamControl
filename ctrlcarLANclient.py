#!/usr/bin/python3

#клиентская часть

from doctest import testsource
import keyboard     #импорт библиотеки для работы с клавой
import socket
import time
import sys
import cv2 as cv

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.237', 8089))
########################################################################## 
def test(x):
    if x.event_type == 'down': 
        if x.name == 'w':
            clientsocket.send(f'w'.encode('utf-8'))
        elif x.name == 's':
            clientsocket.send(f's'.encode('utf-8'))
        elif x.name == 'a':
            clientsocket.send(f'a'.encode('utf-8'))
        elif x.name == 'd':
            clientsocket.send(f'd'.encode('utf-8'))
        elif x.name == 'p':
            clientsocket.send(f'stopthecar'.encode('utf-8'))
            clientsocket.send(f'disconnect'.encode('utf-8'))
        elif x.name == 'z':
            clientsocket.send(f'z'.encode('utf-8'))
        elif x.name == 'x':
            clientsocket.send(f'x'.encode('utf-8'))
        elif x.name == 'c':
            clientsocket.send(f'c'.encode('utf-8'))
        elif x.name == 'v':
            clientsocket.send(f'v'.encode('utf-8'))
        else:
            clientsocket.send(f'stopthecar'.encode('utf-8'))
    elif x.event_type == 'up':
        if x.name == 'r':
            clientsocket.send(f'r'.encode('utf-8'))
        elif x.name == 'f':
            clientsocket.send(f'f'.encode('utf-8'))
        else:
            clientsocket.send(f'stopthecar'.encode('utf-8'))
    else:
        clientsocket.send(f'stopthecar'.encode('utf-8'))
        # print("fdfdfdf")
########################################################################## 

########################################################################## 

keyboard.hook(test)
keyboard.wait("p")
clientsocket.close()
# break