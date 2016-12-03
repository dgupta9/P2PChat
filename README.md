# P2PChat

P2P Chat
-------------
This application allow users to communicate via multiple trackers.

* Requirement:
  Python2.7

* Running Tracker:
  Run tracker by running the command "python tracker.py"

* Running Client:
  Run client by command "python ClientMain.py"

* Registration:
  1) Run tracker
  2) Modify Constants.py to include the IP address of tracker
  3) Run Client
  4) Give any unique userid to register

* Send Message:
  1) After registration, enter '1' to go to send message screen
  2) If client found, enter the message to send
  3) Message delivery status will be shown

* Check Messages:
  1) After registration, enter '2' to go to view my messages
  2) All the messages will be shown here

* Exit
  1) After registration, enter '3' to exit and un register the client
  2) Unregistration confirmation will be shown
 
* Code Explaination:
  1) tracker.py : The codes for trackers implementation. We use dictionary-”hashtable” to store the user id and the corresponding ip address.
  2) ClientMain.py: The codes for client implementation.
  3) ClientNetworkHelper.py: The codes for handling network part implementation.
  4) Constants.py: Codes for constants.
  5) MessageHandler.py: Codes for storing messages in client.
