# Contains all the helper function to register client on 
from socket import *
import ClientMain
import random
import json

def register():
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    for ip in ClientMain.trackerList:
        randID = str(random.randint(0, 65535))
        flags = 0
        #message = randID + " " + ClientMain.flags + ClientMain.REGISTER + " " + 
        
        ml = [1,2,3,4,5,6]
        ml[0]=randID
        ml[1]=0#ClientMain.flags
        ml[2]=ClientMain.REGISTER
        ml[3]="1.1.1.1"#IP ADDRESS
        ml[4]=ClientMain.userid
        message = json.dumps(ml)
        clientSocket.sendto(message.encode(),(ip, ClientMain.trackerPort))
        ClientMain.trackerPort