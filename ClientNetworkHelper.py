# this module handles all N/W communication

import pickle
import Constants
from socket import *
import random
import ClientMain

AddErr = True

def decodeMessage(data):
    # decode the data and return list
    try:
        return pickle.loads(data)
    except:
        return None

def encodeMessage(data,addParity=False):
    # decode the data and return list
        global AddErr
    #try:
        #print pickle.dumps(data)
        encodedMsg = pickle.dumps(data)
        if(addParity):
            parityVal =  calculateParity(encodedMsg)
            print "Parity:"+str(parityVal)
            if AddErr:
                encodedMsg = list(encodedMsg)
                firstChar = encodedMsg[0]
                nval = ord(firstChar)
                nval+=1
                firstChar = chr(nval)
                encodedMsg[0] = firstChar
                encodedMsg = ''.join(encodedMsg);
                AddErr = False
            return encodedMsg+str(parityVal)
        else:
            return encodedMsg
    #except:
    #    return None

def calculateParity(data):
    # calculates the parity of the data
    pVal = 0
    data = list(data)
    for byte in data:
        val = ord(byte)
        for i in range(8):
            if val&1:
                pVal = (pVal+1)%2
            val = val>>1
    return pVal
        
def validateRecvMessage(recvData,userId):
    # validates headers in message
    if(recvData[1] != userId):
        return False
    return True

def recvThread(mh,userId):
    # mh is an instance of MessageHandler
    serverPort = Constants.clientPort
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(1)
    while True:
        connectionSocket, addr = serverSocket.accept()
        data = connectionSocket.recv(2048)
        data = decodeMessage(data)
        
        if not validateRecvMessage(data,userId):
            #send error message to client
            respdata = []
            respdata.append(userId)
            respdata.append(data[0])
            respdata.append(data[2])
            if data[3] == Constants.CLIENT_PING_REQ_TYPE:
                respdata.append(Constants.CLIENT_PING_RES_TYPE)
            elif data[3] == Constants.CLIENT_SEND_TYPE:
                respdata.append(Constants.CLIENT_RECV_TYPE)
            else:
                #close connection for unknowm messages type
                connectionSocket.close()
                continue
            
            respdata.append(len(Constants.CLIENT_PING_RES_WRNG_MSG))
            respdata.append(Constants.CLIENT_PING_RES_WRNG_MSG)
            respdata = encodeMessage(respdata)
            connectionSocket.send(respdata)
            connectionSocket.close()
            continue
        
        if data[3] == Constants.CLIENT_PING_REQ_TYPE:
            respdata = []
            respdata.append(userId)
            respdata.append(data[0])
            respdata.append(data[2])
            respdata.append(Constants.CLIENT_PING_RES_TYPE)
            respdata.append(len(Constants.CLIENT_PING_RES_OK_MSG))
            respdata.append(Constants.CLIENT_PING_RES_OK_MSG)
            respdata = encodeMessage(respdata)
            connectionSocket.send(respdata)

        
        if data[3] == Constants.CLIENT_SEND_TYPE:
            mh.addMessage(data[0],data[5])
            #send back the ok
            respdata = []
            respdata.append(data[1])
            respdata.append(data[0])
            respdata.append(data[2])
            respdata.append(Constants.CLIENT_RECV_TYPE)
            respdata.append(len(Constants.CLIENT_PING_RES_OK_MSG))
            respdata.append(Constants.CLIENT_PING_RES_OK_MSG)
            respdata = encodeMessage(respdata)
            connectionSocket.send(respdata)
        
        connectionSocket.close()
    
def pingReq(myuserid,destuserid,destipaddress):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((destipaddress, Constants.clientPort))
    data = []
    data.append(myuserid)
    data.append(destuserid)
    randID = str(random.randint(0, 65535))
    data.append(randID)
    data.append(Constants.CLIENT_PING_REQ_TYPE)
    data.append(len(Constants.CLIENT_PING_REQ_MSG))
    data.append(Constants.CLIENT_PING_REQ_MSG)
    data = encodeMessage(data)
    client_socket.send(data)
    
    # check is message is received
    recvStatus = False
    data = client_socket.recv(1024)
    data = decodeMessage(data)
    print "pingReq"
    print data
    if (data[0] == destuserid) and (data[1] == myuserid):
        if data[2] == randID:
            if data[5] == Constants.CLIENT_PING_RES_OK_MSG:
                recvStatus = True
    client_socket.close()
    return recvStatus

def sendMsg(message,senderId, recvId,recvIpaddress):
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((recvIpaddress, Constants.clientPort))
    data = []
    data.append(senderId)
    data.append(recvId)
    randID = str(random.randint(0, 65535))
    data.append(randID)
    data.append(Constants.CLIENT_SEND_TYPE)
    data.append(len(message))
    data.append(message)
    data = encodeMessage(data)
    client_socket.send(data)
    
    # check is message is received
    recvStatus = False
    data = client_socket.recv(1024)
    data = decodeMessage(data)
    if (data[0] == recvId) and (data[1] == senderId):
        if data[2] == randID:
            if data[3] == Constants.CLIENT_RECV_TYPE:
                recvStatus = True
    client_socket.close()
    return recvStatus
    
def trackerQuery(userid,trackerList):
    randID = 0
    i=1
    for ip in trackerList:
        randID = str(random.randint(0, 65535))
        ml = []
        ml.append(randID)
        ml.append(Constants.REQ_FLAG)
        ml.append(Constants.QUERY)
        ml.append("")
        ml.append(userid)
        message = encodeMessage(ml,addParity=True)
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(message.encode(),(ip, Constants.trackerPort))
        
        serverResp, serverAddress = clientSocket.recvfrom(2048)
        
        serverResp = serverResp.decode()
        serverResp = decodeMessage(serverResp)
        
        if serverResp[1]&Constants.MSG_ERR:
            #error , resend packet
            print "SERVER GOT ERROR"
            return trackerQuery(userid,trackerList)
        
        if serverResp[0] == randID:
            # check for response flag
            if serverResp[1]&Constants.RES_FLAG:
                if serverResp[1]&Constants.USERNEXIST_FLAG:
                    #name doesn't occured
                    print "USER NOT FOUND TRACKER ["+str(i)+"]"
                    i+=1
                else:
                    if serverResp[4] ==userid:
                        return serverResp[3]
                    
    return None
    
def exitTracker(userid,trackerList):
    i=0
    randID = 0
    for ip in trackerList:
        randID = str(random.randint(0, 65535))
        ml = []
        ml.append(randID)
        ml.append(Constants.REQ_FLAG)
        ml.append(Constants.EXIT)
        ml.append("")
        ml.append(userid)
        message = encodeMessage(ml,addParity=True)
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        clientSocket.sendto(message.encode(),(ip, Constants.trackerPort))
        
        serverResp, serverAddress = clientSocket.recvfrom(2048)
        clientSocket.close()
        serverResp = serverResp.decode()
        serverResp = pickle.loads(serverResp)
        
        if serverResp[1]&Constants.MSG_ERR:
            #error , resend packet
            print "SERVER GOT ERROR"
            return exitTracker(userid,trackerList)
        
        if serverResp[0] == randID:
            # check for response flag
            if serverResp[1]&Constants.RES_FLAG:
                if serverResp[2]&Constants.EXIT:
                    return
    
    #assumes none of the server has this client's information          
    return
    
def register(userid,trackerList):
    i=0
    randID = 0
    myIPAddr = gethostbyname(gethostname());
    for ip in trackerList:
        randID = str(random.randint(0, 65535))
        ml = []
        ml.append(randID)
        ml.append(Constants.REQ_FLAG)
        ml.append(Constants.REGISTER)
        ml.append(myIPAddr)
        ml.append(userid)
        message = encodeMessage(ml,addParity=True)
        try:
            clientSocket=socket(AF_INET, SOCK_DGRAM)
            clientSocket.sendto(message.encode(),(ip, Constants.trackerPort))
            serverResp, serverAddress = clientSocket.recvfrom(2048)
            clientSocket.close()
        except:
            return None
        i+=1
        if serverResp == '':
            continue
        serverResp = serverResp.decode()
        serverResp = decodeMessage(serverResp)
        print "RESPONSE"
        print serverResp
        if serverResp[1]&Constants.MSG_ERR:
            #error , resend packet
            print "SERVER GOT ERROR"
            return register(userid,trackerList)
            #return register(userid,trackerList)
            
        if serverResp[0] == randID:
            # check for response flag
            if serverResp[1]&Constants.RES_FLAG:
                if serverResp[1]&Constants.SERVER_FULL:
                    #server is full goto next one
                    print "server full"
                    continue
                if serverResp[1]&Constants.NCONFLICT_FLAG:
                    #name conflict occured
                    print "UserId already Exits, try another one"
                    userid = ClientMain.getUserLoginID()
                    return register(userid,trackerList)
                # TODO : check why here
                #if serverResp[4] != userid:
                #    register(userid)
                return myIPAddr
                # client successfully registered
    return None        
