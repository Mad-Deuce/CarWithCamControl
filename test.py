from array import *
import time

while True:
    SpeedTi=3
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
    for i in range (8):
        SpeedOut=(SpeedT[2]>>i) & 0b00000001
        print(SpeedOut)
        time.sleep(1)