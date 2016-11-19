# Contains all the helper function to register client on 
from socket import *
import ClientMain
import random
import pickle
nodeIPMap = dict()

def query(userid):
    clientSocket = []
    i=0
    randID = 0
    for ip in ClientMain.trackerList:
        randID = str(random.randint(0, 65535))
        ml = []
        ml.append(randID)
        ml.append(ClientMain.REQ_FLAG)
        ml.append(ClientMain.QUERY)
        ml.append("")
        ml.append(userid)
        message = pickle.dumps(ml)
        clientSocket.append(socket(AF_INET, SOCK_DGRAM))
        clientSocket[i].sendto(message.encode(),(ip, ClientMain.trackerPort))
        i+=1
        
    for i in range(3):
        serverResp, serverAddress = clientSocket[i].recvfrom(2048)
        if serverResp == '':
            continue
        serverResp = serverResp.decode()
        serverResp = pickle.loads(serverResp)
        print "RESPONSE"
        print serverResp
        if serverResp[0] == randID:
            # check for response flag
            if serverResp[1]&ClientMain.RES_FLAG:
                if serverResp[1]&ClientMain.USERNEXIST_FLAG:
                    #name conflict occured
                    print "USER NOT FOUND"
                
                
                # TODO : check why here
                #if serverResp[4] != userid:
                #    register(userid)
                return

def exit(userid):
    clientSocket = []
    i=0
    randID = 0
    for ip in ClientMain.trackerList:
        randID = str(random.randint(0, 65535))
        ml = []
        ml.append(randID)
        ml.append(ClientMain.REQ_FLAG)
        ml.append(ClientMain.EXIT)
        ml.append("")
        ml.append(userid)
        message = pickle.dumps(ml)
        clientSocket.append(socket(AF_INET, SOCK_DGRAM))
        clientSocket[i].sendto(message.encode(),(ip, ClientMain.trackerPort))
        i+=1
    
    for i in range(3):
        serverResp, serverAddress = clientSocket[i].recvfrom(2048)
        if serverResp == '':
            continue
        serverResp = serverResp.decode()
        serverResp = pickle.loads(serverResp)
        print "RESPONSE"
        print serverResp


def register(userid):
    clientSocket = []
    i=0
    randID = 0
    for ip in ClientMain.trackerList:
        randID = str(random.randint(0, 65535))
        ml = []
        ml.append(randID)
        ml.append(ClientMain.REQ_FLAG)
        ml.append(ClientMain.REGISTER)
        ml.append(gethostbyname(gethostname()))
        ml.append(userid)
        message = pickle.dumps(ml)
        clientSocket.append(socket(AF_INET, SOCK_DGRAM))
        clientSocket[i].sendto(message.encode(),(ip, ClientMain.trackerPort))
        i+=1
    
    for i in range(3):
        serverResp, serverAddress = clientSocket[i].recvfrom(2048)
        if serverResp == '':
            continue
        serverResp = serverResp.decode()
        serverResp = pickle.loads(serverResp)
        print "RESPONSE"
        print serverResp
        if serverResp[0] == randID:
            # check for response flag
            if serverResp[1]&ClientMain.RES_FLAG:
                if serverResp[1]&ClientMain.NCONFLICT_FLAG:
                    #name conflict occured
                    print "UserId already Exits, try another one"
                    userid = ClientMain.getUserLoginID()
                    register(userid)
                # TODO : check why here
                #if serverResp[4] != userid:
                #    register(userid)
                return
                # client successfully registered
        
    