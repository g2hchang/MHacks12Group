#!/usr/bin/python
from serial import Serial
import re
import os
import requests

def processLine(segments, index):
    split = segments[index].split(": ")
    return split[1]


def sendRequestForSensorValue(sensorVal):
    getString1 = "https://mhacks12.herokuapp.com/update/1/" + sensorVal
    getString = "https://mhacks12.herokuapp.com/update-realtime/1/" + sensorVal
    #getString = "https://73b1b781.ngrok.io/update-realtime/1/" + sensorVal
    requests.get(getString)
    print getString


def main():  
    serialConn = Serial("/dev/ttyACM0", 9600)
    serialConn.flushInput()
    
    while True:
        line = (serialConn.readline())
        line = line.strip()
        if (len(line) > 0 and line[0] == "I"):         
            segments = line.split(", ")
            idVal = processLine(segments, 0) 
            timestampMillis = processLine(segments, 1) 
            sensorVal = processLine(segments, 2)
            sensorValTimeAvg = processLine(segments, 3)
            if (sensorVal.isdigit()):
                #sensorVal = str(int((float(sensorVal) / 1024) * 100))
                sendRequestForSensorValue(max(sensorVal, 0))
            serialConn.flushInput()

if __name__ == '__main__':
    main()
