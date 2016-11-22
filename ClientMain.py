import ClientRegister
import thread

userid = ""
myIPAddr = ""

# store mapping of client user id to IP address
ClientIPCacheMap = {}

#tracker list
trackerList = ["127.0.0.1"]#,"1.1.1.2","1.1.1.3"]
trackerPort = 9990

#client port
clientPort = 7070

#FLAG VALUES
REQ_FLAG =0
RES_FLAG = 128
NCONFLICT_FLAG = 64
USERNEXIST_FLAG = 32
EXIT_FLAG = 16
SERVER_FULL = 8


#CLIENT MESSAGE TYPES
CLIENT_PING_REQ_TYPE = 1
CLIENT_PING_RES_TYPE = 2
CLIENT_SEND_TYPE = 3
CLIENT_RECV_TYPE = 4

#CLIENT MESSAGE VALUES
CLIENT_PING_REQ_MSG = "HELLO"
CLIENT_PING_RES_OK_MSG = "OK"
CLIENT_PING_RES_BUSY_MSG = "BUSY"


#ACTION VALUES
REGISTER = 0
QUERY = 1
EXIT = 2
SENDMESSAGE = 4
REPLYSTATUS = 8

# message list
msgList = []


def showMainScreen():
    welcomeMsg = """\n    #################################
    #                               #
    #      P2P CHAT APLICATION      #
    #                               #
    #################################"""
    print welcomeMsg
    
def showMainOptions():
    global userid
    print "\n\n1. Send Messages\n2. My Messages\n3. Quit"
    while True:
        option = raw_input("\nEnter choice[1,2,3]: ")
        if option == '3':
            ClientRegister.exit(userid)
            break
        elif option == '2':
            printMyMessages()# read message
        elif option == '1':
            showSendScreen()

def printMyMessages():
    #global msgList
    print "Messages below:"
    for item in ClientRegister.returnMsg():
        print item


def showSendScreen():
    global userid
    targetID = raw_input("Enter the user's id to send message:")
    destIPAddr = ClientRegister.query(targetID)
    destIPAddr = '127.0.0.1'
    if destIPAddr == None:
        print "User id not found"
        return
        
    #send ping request first
    targetAlive = ClientRegister.pingReq(userid,targetID,destIPAddr)
    if not targetAlive:
        print "User ["+targetID+"] not online"
        return
    message = raw_input("Enter the message:")
    if ClientRegister.sendMsg(message,userid,targetID,destIPAddr):
        print "Message send successfully"

    
def getUserLoginID():
    #print 
    global userid
    userid = raw_input("Enter your user id : ")
    return userid

def addMessage(msgItem):
    global msgList
    msgList.append(msgItem)
    
if __name__ == "__main__":
    showMainScreen()
    userid = getUserLoginID()
    thread.start_new_thread(ClientRegister.recvThread,())
    print "\n\n Welcome "+userid+" !"
    myIPAddr = ClientRegister.register(userid)
    showMainOptions()