import ClientNetworkHelper
import thread
from MessageHandler import MessageHandler
import Constants
import sys
userid = ""
myIPAddr = ""
mh = None

# store mapping of client user id to IP address
ClientIPCacheMap = {}


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
            ClientNetworkHelper.exitTracker(userid,Constants.trackerList)
            break
        elif option == '2':
            printMyMessages()# read message
        elif option == '1':
            showSendScreen()

def printMyMessages():
    global mh
    print "Messages below:"
    mh.printAllMessages()


def showSendScreen():
    global userid
    targetID = raw_input("Enter the user's id to send message:")
    destIPAddr = ClientNetworkHelper.trackerQuery(targetID,Constants.trackerList)
    if destIPAddr == None:
        print "User id not found"
        return
        
    #send ping request first
    targetAlive = ClientNetworkHelper.pingReq(userid,targetID,destIPAddr)
    if not targetAlive:
        print "User ["+targetID+"] not online"
        return
    message = raw_input("Enter the message:")
    if ClientNetworkHelper.sendMsg(message,userid,targetID,destIPAddr):
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
    print "\n\n Welcome "+userid+" !"
    myIPAddr = ClientNetworkHelper.register(userid,Constants.trackerList)
    if myIPAddr is None:
        print "Failed to connect to any tracker / All trackers are full"
        sys.exit(0)
    mh = MessageHandler()
    thread.start_new_thread(ClientNetworkHelper.recvThread,(mh,userid))
    showMainOptions()