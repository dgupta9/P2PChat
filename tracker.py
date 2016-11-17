import json
from socket import *
serverPort = 9990
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print ("The server is ready to receive")
namelist=[]
iplist=[]
nodeIPmap=dict()
messagelist=[1,2,3,4,5]
sendbackcontrol=0


def checkactions(action, clname,clip):
	global namelist
	global iplist
	global sendbackcontrol
	if action==0:
		if clname in namelist:              #name conflict, sendbackcontrol=2
			sendbackcontrol=2
		elif len(namelist)>=5:              #more than 5 clients exist, need to check other trackers. sendbackcontrol=3
			sendbackcontrol=3
		else:
			namelist.append(clname)
			iplist.append(clip)
			sendbackcontrol=1







while True:
	message, clientAddress = serverSocket.recvfrom(2048)
	messagelist=json.loads(message)
	print "Received "
	print messagelist
	print "name"
	print namelist
	print "ip"
	print iplist
	checkactions(messagelist[2],messagelist[4],messagelist[3])
	if sendbackcontrol==1:
		responsemessage=[messagelist[0],0,0,messagelist[3],messagelist[4]]
		response = json.dumps(responsemessage)
		serverSocket.sendto(response, clientAddress)
	elif sendbackcontrol==2:
		responsemessage = [messagelist[0], 128, 0, messagelist[3], messagelist[4]]
		response = json.dumps(responsemessage)
		serverSocket.sendto(response, clientAddress)

	continue




