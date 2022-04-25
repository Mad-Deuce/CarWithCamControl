import cv2 as cv
import socket
import os

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('192.168.1.237', 8090))
serversocket.listen(1) # become a server socket, maximum 5 connections

capture = cv.VideoCapture(-1)
while True:
    connection, address = serversocket.accept()

    if not (capture.isOpened()):
        print('Could not open video device')
    else:
        while True:
            #capture = cv.VideoCapture(0)
            # cv.WaitKey(100)
            
            ret, frame = capture.read()
            cv.waitKey(1000)
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            size=(160,120)
            out = cv.resize(gray,size)
            
            print(out.size)
            #connection.send(out.size)
            frameLen=out.size
            byteFrameLen=frameLen.to_bytes(4, 'little', signed=False)
            connection.send(byteFrameLen)
            # >>>i_num = 123
            # >>>b_num = i_num.to_bytes(2, 'little', signed=False)
            # >>>b_num
            # b'{\x00'


            cv.imwrite("capture.png", out)
            f = open ("capture.png", "rb")


            #with open("capture.png", "ab") as mifile:

            #f=out.tobytes()
            #f = open (out, "rb")
            #cv.imshow('frame',out)
            midata = f.read(1024)
            while midata:
                connection.send(midata)
                midata = f.read(1024)
            #cv.waitKey(50)
            #connection.send(f'endframe'.encode('utf-8'))
            #os.remove(f)
            print("endfile")
            f.close()
            os.remove("capture.png")
            

            
