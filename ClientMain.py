import ClientRegister

userid = ""

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

#ACTION VALUES
REGISTER = 0
QUERY = 1
EXIT = 2
SENDMESSAGE = 4
REPLYSTATUS = 8


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
    option = raw_input("\nEnter choice[1,2,3]: ")
    if(option == '3'):
        ClientRegister.exit(userid)
    elif option == '1':
        showSendScreen()

def showSendScreen():
    target = raw_input("Enter the user's id to send message:")
    ClientRegister.query(target)
    
    
def getUserLoginID():
    #print 
    global userid
    userid = raw_input("Enter your user id : ")
    return userid

if __name__ == "__main__":
    showMainScreen()
    userid = getUserLoginID()
    print "\n\n Welcome "+userid+" !"
    ClientRegister.register(userid)
    showMainOptions()