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
                return serverResp[3]

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
    myIPAddr = gethostbyname(gethostname());
    for ip in ClientMain.trackerList:
        randID = str(random.randint(0, 65535))
        ml = []
        ml.append(randID)
        ml.append(ClientMain.REQ_FLAG)
        ml.append(ClientMain.REGISTER)
        ml.append(myIPAddr)
        ml.append(userid)
        message = pickle.dumps(ml)
        clientSocket.append(socket(AF_INET, SOCK_DGRAM))
        clientSocket[i].sendto(message.encode(),(ip, ClientMain.trackerPort))
        i+=1
    
    for i in range(3):
        serverResp, serverAddress = clientSocket[i].recvfrom(2048)
        clientSocket[i].close()
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
                    return register(userid)
                # TODO : check why here
                #if serverResp[4] != userid:
                #    register(userid)
                return myIPAddr
                # client successfully registered
     
def pingReq(myuserid,destuserid,destipaddress):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((destipaddress, ClientMain.clientPort))
    data = []
    data.append(myuserid)
    data.append(destuserid)
    randID = str(random.randint(0, 65535))
    data.append(randID)
    data.append(ClientMain.CLIENT_PING_REQ_TYPE)
    data.append(len(ClientMain.CLIENT_PING_REQ_MSG))
    data.append(ClientMain.CLIENT_PING_REQ_MSG)
    data = pickle.dumps(data)
    client_socket.send(data)
    
    # check is message is received
    recvStatus = False
    data = client_socket.recv(1024)
    print "IP GOT RESP:"+data
    data = pickle.loads(data)
    if (data[0] == destuserid) and (data[1] == myuserid):
        if data[2] == randID:
            if data[3] == CLIENT_PING_RES_OK_MSG:
                recvStatus = True
    client_socket.close()
    return recvStatus

def sendMsg(message,myuserid, destuserid,ipaddress):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((ipaddress, ClientMain.clientPort))
    data = []
    data.append(myuserid)
    data.append(destuserid)
    randID = str(random.randint(0, 65535))
    data.append(randID)
    data.append(ClientMain.CLIENT_SEND_TYPE)
    data.append(len(message))
    data.append(message)
    data = pickle.dumps(data)
    client_socket.send(data)
    
    # check is message is received
    recvStatus = False
    data = client_socket.recv(1024)
    print "SEND GOT RESP:"+data
    data = pickle.loads(data)
    if (data[0] == destuserid) and (data[1] == myuserid):
        if data[2] == randID:
            if data[3] == CLIENT_RECV_TYPE:
                recvStatus = True
    client_socket.close()
    return recvStatus
    
    
def RecvThread():
    pass