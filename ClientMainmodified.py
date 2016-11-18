import ClientRegister


userid = ""

# store mapping of client user id to IP address
ClientIPCacheMap = {}

#tracker list
trackerList = ["10.139.58.108"]#,"1.1.1.2","1.1.1.3"]
trackerPort = 9990

#FLAG VALUES
RES_FLAG = 128
NCONFLICT_FLAG = 64

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
    print "\n\n1. Send Messages\n2. My Messages\n3. Quit"
    option = raw_input("\nEnter choice[1,2,3]: ")
    if(option == '3'):
        return
    elif option == '1':
        pass
        
    
def getUserLoginID():
    #print 
    global userid
    userid = raw_input("Enter your user id : ")

if __name__ == "__main__":
    showMainScreen()
    getUserLoginID()
    print "\n\n Welcome "+userid+" !"
    ClientRegister.register()
    showMainOptions()