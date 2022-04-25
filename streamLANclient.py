#from asyncio.windows_events import NULL
import socket
import cv2 as cv
import os

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.237', 8090))

while True:
    with open("mi2.png", "ab") as mifile:
        data = clientsocket.recv(1024)
        if len(data) == 4:
            byteFrameLen=data

            frameLen=int.from_bytes(byteFrameLen, 'little', signed=False)
        
            print(frameLen)
        elif len(data) > 4:
            framedata=''
            while data:
                if len(framedata)==frameLen:
                    print("lengthend")
                    break
                framedata+=data
                #framedata+=data
                #mifile.write(data)
                data = clientsocket.recv(1024)
                print("ass")
            #cv.imshow('frame',mifile)
            mifile.write(framedata)
            print("bss")
            mifile.close()
            os.remove("mi2.png")