# This module maintains List of message received by client

class MessageHandler:
    
    # message list
    msgList = []
    
    def __init__(self):
        self.msgList = []
    
    def addMessage(self,senderID, messageContent):
        #this function add the message tuple in list
        from time import gmtime, strftime
        timeStamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        msgItem = (senderID, timeStamp, messageContent)
        self.msgList.append(msgItem)
    
    def getMessageCount(self):
        # return the messages in the list
        return len(self.msgList)
    
    def getMessage(self, pos):
        # returns the messages at position
        if pos>=len(self.msgList):
            return None
        return self.msgList[pos];
    
    def printAllMessages(self):
        #this function prints all messages
        if len(self.msgList)==0:
            print "NO MESSAGES TO PRINT"
            return
        
        print "\nMESSAGES ["+str(len(self.msgList))+"]:"
        index=1
        for msgItem in self.msgList:
            print "\n("+str(index)+")"
            print "\nFROM : "+str(msgItem[0])
            print "\nTIME : "+str(msgItem[1])
            print "\nMESSAGE : "+str(msgItem[2])
            index+=1
        