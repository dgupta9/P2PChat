import json
import pickle
from socket import *
serverPort = 9990
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
namelist=[]
iplist=[]
hashtable={}
nodeIPmap=dict()
messagelist=[1,2,3,4,5]
sendbackcontrol=0






def showMainScreen():
    welcomeMsg = """\n    #################################
    #                               #
    #      P2P CHAT Tracker         #
    #                               #
    #################################"""
    print welcomeMsg



def checkactions(action, clname,clip):
	global namelist
	global iplist
	global sendbackcontrol
	global clientAddress
	if action==0:							#registration
		if clname in namelist:              #name conflict, sendbackcontrol=2
			sendbackcontrol=2

		elif len(namelist)>=5:              #more than 5 clients exist, need to check other trackers. sendbackcontrol=3
			sendbackcontrol=3
		else:                               #successful registration, sendbackcontrol=1
			namelist.append(clname)
			iplist.append(clientAddress[0])
			hashtable[clname]=clientAddress[0]
			sendbackcontrol=1
	elif action==1:                         #request
		if clname in namelist:              #name found in tracker, sendbackcontrol=4
			sendbackcontrol=4
		else:
			sendbackcontrol=5               #name not found, sendbackcontrol=5
	elif action==2:                         #exit
		if clname in  namelist:
			sendbackcontrol=6				#name found,sendbackcontrol=6
		else:
			sendbackcontrol=7				#name not found, error,sendbackcontrol=6





def response(a):
	if a == 1:
		responsemessage = [messagelist[0], 128, 0, messagelist[3], messagelist[4]]		#Registration: successful registration,flags=10000000,action=0
		response = pickle.dumps(responsemessage)
		serverSocket.sendto(response.encode(), clientAddress)
		print "The user has registered successfully"

	elif a== 2:
		responsemessage = [messagelist[0], 192, 0, messagelist[3], messagelist[4]]		#Registration: if there is a name confliction, flags=11000000, action=0
		response = pickle.dumps(responsemessage)
		serverSocket.sendto(response.encode(), clientAddress)
		print "User name confliction"

	elif a==3:
		responsemessage = [messagelist[0], 136, 0, messagelist[3],messagelist[4]]       # Registration: if there is no space in database, flags=11001000, action=0
		response = pickle.dumps(responsemessage)
		serverSocket.sendto(response.encode(), clientAddress)
		print "User name confliction"

	elif a==4:
		position=namelist.index(messagelist[4])
		desiredip=iplist[position]
		responsemessage = [messagelist[0], 128, 1,desiredip, messagelist[4]]             #Request: name found, sent successfully, flag=10000000,action=1
		response = pickle.dumps(responsemessage)
		serverSocket.sendto(response.encode(), clientAddress)
		print "Name found, sent successfully"

	elif a==5:
		responsemessage = [messagelist[0], 160, 1, messagelist[3],messagelist[4]]		#Request: if name not existing, flags=10100000,action=1
		response = pickle.dumps(responsemessage)
		serverSocket.sendto(response.encode(), clientAddress)
		print "Name not found"

	elif a==6:																			#Exit: if name found, flag=10000000, action=2
		position = namelist.index(messagelist[4])
		namelist.remove(messagelist[4])
		del iplist[position]
		del hashtable[messagelist[4]]
		responsemessage = [messagelist[0], 128, 2, messagelist[3], messagelist[4]]
		response = pickle.dumps(responsemessage)
		serverSocket.sendto(response.encode(), clientAddress)
		print "Exit Successfully"

	elif a==7:																			#Exit: if name not exsisting, flag=10010000,action=2
		responsemessage = [messagelist[0], 144, 2, messagelist[3],messagelist[4]]
		response = pickle.dumps(responsemessage)
		serverSocket.sendto(response.encode(), clientAddress)
		print "ERROR:Name not found"



if __name__ == "__main__":
	showMainScreen()
	print "The server is ready to receive"
	while True:
		m1, clientAddress = serverSocket.recvfrom(2048)
		#message=message.decode()
		messagelist=pickle.loads(m1)
		print "Received "
		print messagelist

		checkactions(messagelist[2],messagelist[4],messagelist[3])
		response(sendbackcontrol)
		print "name => ip"
		for key, value in hashtable.iteritems():
			print key, '=>',value

		continue




