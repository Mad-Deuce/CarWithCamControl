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
            # print(x.name)
        elif x.name == 's':
            clientsocket.send(f's'.encode('utf-8'))
            # print("s was pressed")
        elif x.name == 'a':
            clientsocket.send(f'a'.encode('utf-8'))
            # print("a was pressed")
        elif x.name == 'd':
            clientsocket.send(f'd'.encode('utf-8'))
            # print("d was pressed")
        elif x.name == 'p':
            # print("p was pressed")
            clientsocket.send(f'stopthecar'.encode('utf-8'))
            clientsocket.send(f'disconnect'.encode('utf-8'))
            #capture.release()
            #cv.destroyAllWindows()
        else:
            clientsocket.send(f'stopthecar'.encode('utf-8'))
            # print(x.name)
            # print("fdfdfdf")
    else:
        clientsocket.send(f'stopthecar'.encode('utf-8'))
        # print("fdfdfdf")
########################################################################## 

########################################################################## 
#capture = cv.VideoCapture(0)
#capture = clientsocket.recv(64)
#with open("mi2.png", "ab") as mifile:
#    data = clientsocket.recv(1024)
#    while data:
#        mifile.write(data)
#        data = clientsocket.recv(1024)
    #out=mifile.read()
#keyboard.add_hotkey("w", lambda: clientsocket.send(f'w'.encode('utf-8')))
#keyboard.add_hotkey("w", lambda: print("w was pressed"))
#keyboard.add_hotkey("w", lambda: test)
#keyboard.add_hotkey("w", test)
#keyboard.add_hotkey("w", test,args=keyboard.hook_key("w"))
#keyboard.add_hotkey("w", test,args=(keyboard.KeyboardEvent("down",28,"enter")))
# while(True):
#     if keyboard.is_pressed("w"):
#         print("w was pressed")
#         clientsocket.send(f'w'.encode('utf-8'))
#     # if keyboard.is_pressed('s'):
#     #     clientsocket.send(f's'.encode('utf-8'))
#     # if keyboard.is_pressed('a'):
#     #     clientsocket.send(f'a'.encode('utf-8'))
#     # if keyboard.is_pressed('d'):
#     #     clientsocket.send(f'd'.encode('utf-8'))
#     if keyboard.is_pressed('p'):
#         clientsocket.send(f'disconnect'.encode('utf-8'))
#         clientsocket.close()
    # clientsocket.send(f'stopthecar'.encode('utf-8'))
    #ret, frame = capture.read()
    #ret, frame = capture
    #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #size=(160,120)
    #out = cv.resize(gray,size)
# with open("mi2.png", "ab") as mifile:
#     data = clientsocket.recv(1024)
#     while data:
#         mifile.write(data)
#         data = clientsocket.recv(1024)
    # cv.imshow('frame',mifile)
#    if cv.waitKey(1) & 0xFF == ord('q'):
#        break
#+capture.release()
#+cv.destroyAllWindows()
    #keyboard.add_hotkey("w", lambda: print("ctrl+alt+j was pressed"))
keyboard.hook(test)
keyboard.wait("p")
clientsocket.close()
# break