# -*- coding: utf-8 -*-

import serial

import struct
ser = serial.Serial("COM6",baudrate = 9600,timeout = 200)
def func(dist):

    while 1:
        data1=ser.readline()
        l1=len(data1)
        if l1-1<=1:
            if data1[0]<dist[0]:
                #print("Helllllooo")
                print("Moving towards us",data1)
                func(data1)
            else:
                print("moving away")

def func1(dist):

    while 1:
        x=dist
        data1=ser.readline()
        l1=len(data1)
        if l1-1==2 :
       # print("hi")
            if data1[0]<x[0]:
                print("Moving towards us",data1)
                func1(data1)
        elif l1-1 ==1:
            print("Moving towards us")
            func1(data1)

        else:
            print("Moving away")

def se() :

    while 1:
        data = ser.readline()
    #print(data[:-1])
        l=len(data)
        data=data[:-1]
        if l-1 == 1:
            if data[0]>52 and data[0]<=57:
                print("Object found")
                func(data)
        elif l-1 == 2:
            print("Object found")
            func1(data)
if __name__ == '__main__':
    se()
