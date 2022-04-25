#from asyncio.windows_events import NULL
import socket
import cv2 as cv
import os

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.1.237', 8090))

iterffss=0
while True:
    flnm="capture.jpeg"
    with open(flnm, "ab") as mifile:
        mifile.seek(0)
        data = clientsocket.recv(1024)

        if len(data) == 4:
            byteFrameLen=data
            frameLen=int.from_bytes(byteFrameLen, 'little', signed=False)
            print(frameLen)

            data = clientsocket.recv(1024)

            framedataLen=0
            while data:
                framedataLen+=len(data)
                mifile.write(data)
                if framedataLen>=frameLen:
                    print(framedataLen)
                    print("lengthend")
                    iterffss=iterffss+1
                    print(iterffss)
                    break
                #print(1)
                clientsocket.settimeout(1)
                data = clientsocket.recv(1024)
                #print("recivepart")
                #print(2)
            #print("allfilerecive")
            
            mifile.close()
            #print(3)
            cv.imshow('frame',cv.imread(flnm))
            #print(4)
            cv.waitKey(25)
            #print(5)
            #break           #ddddddddddddddddddddddddd
            os.remove(flnm)
            #print(6)