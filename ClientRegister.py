# Contains all the helper function to register client on 
from socket import *
import ClientMain
import random
import pickle
from time import gmtime, strftime
nodeIPMap = dict()

msgList = []

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
        
    for i in range(len(ClientMain.trackerList)):
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
    
    for i in range(len(ClientMain.trackerList)):
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
    data = pickle.loads(data)
    print "PING RESP:"
    print data
    if (data[0] == destuserid) and (data[1] == myuserid):
        if data[2] == randID:
            if data[5] == ClientMain.CLIENT_PING_RES_OK_MSG:
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
            if data[3] == ClientMain.CLIENT_RECV_TYPE:
                recvStatus = True
    client_socket.close()
    return recvStatus
    
def returnMsg():
    global msgList
    return msgList
    
def recvThread():
    serverPort = ClientMain.clientPort
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    global msgList
    while True:
        connectionSocket, addr = serverSocket.accept()
        data = connectionSocket.recv(2048)
        print "Recver got :"+data
        recvStatus= False
        data = pickle.loads(data)
        print data
            # ADD more check of destn
        if data[3] == ClientMain.CLIENT_PING_REQ_TYPE:
            #send back OK
            respdata = []
            respdata.append(data[1])
            respdata.append(data[0])
            respdata.append(data[2])
            respdata.append(ClientMain.CLIENT_PING_RES_TYPE)
            respdata.append(len(ClientMain.CLIENT_PING_RES_OK_MSG))
            respdata.append(ClientMain.CLIENT_PING_RES_OK_MSG)
            respdata = pickle.dumps(respdata)
            print "RECV THREAD SEND : "+respdata
            connectionSocket.send(respdata)

        
        if data[3] == ClientMain.CLIENT_SEND_TYPE:
            # for send messages
            msgitem = (data[0],strftime("%Y-%m-%d %H:%M:%S", gmtime()),data[5])
            print 'adding msg item'
            print msgitem
            ClientMain.addMessage(msgitem)
            msgList.append(msgitem)
            ClientMain.printMyMessages()
            #send back the ok
            respdata = []
            respdata.append(data[1])
            respdata.append(data[0])
            respdata.append(data[2])
            respdata.append(ClientMain.CLIENT_RECV_TYPE)
            respdata.append(len(ClientMain.CLIENT_PING_RES_OK_MSG))
            respdata.append(ClientMain.CLIENT_PING_RES_OK_MSG)
            respdata = pickle.dumps(respdata)
            connectionSocket.send(respdata)
        
        connectionSocket.close()