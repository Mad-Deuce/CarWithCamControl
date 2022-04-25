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
          
            ret, frame = capture.read()
            cv.waitKey(100)
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            #size=(160,120)
            out = cv.resize(gray,(160,120))
            print(out.size)

            flnm="capture.jpeg"
        
            cv.imwrite(flnm, out)
            with open(flnm, "rb") as f:
                # f = open (flnm, "rb")

                file_stats = os.stat(flnm)
                frameLen=file_stats.st_size
                print(frameLen)

                byteFrameLen=frameLen.to_bytes(4, 'little', signed=False)
                
                connection.send(byteFrameLen)

                midata = f.read(1024)
                while midata:
                    connection.send(midata)
                    midata = f.read(1024)

                print("endfile")

            f.close()
            #break
            os.remove(flnm)
        #break
            

            
