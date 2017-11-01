import socket
import threading
import time

#setting up a TCP server
def makeConnection():
	global serversocket
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = input("Please enter your IP address: ")
	port = int(input("The port you would like to use: "))
	serversocket.bind((host, port))
	serversocket.listen(5)
	print("Server started on %s \n" % str((host,port)))

#message listener and transmitter for a single user		
class chatUser(threading.Thread):
	def __init__(self, id, name, address, socket):
		threading.Thread.__init__(self)
		self.id = id
		self.name = name
		self.address = address
		self.socket = socket
		self.runs = True
	def changeName(self):
		if(self.name == ""):
			justConnected = True
		else:
			justConnected = False
			oldName = self.name
		clientsocket = self.socket
		msg = clientsocket.recv(1024)
		newName = str(msg.decode('ascii'))
		self.name = newName
		print("%s is now known as %s\n" % (self.address, newName))
		if(justConnected):
			joinNoti = ("%s connected to the server" %newName)
		else:
			joinNoti = ("%s is now known as %s" % (oldName, newName))
		sendAll(joinNoti, True)
	def quit(self):
		global userNum
		msg = "*** Goodbye, dear user! :') ***"
		self.socket.send(msg.encode('ascii'))
		userNum = userNum-1
		print("%s has quit, deleted his message listener and user" % self.name)
		leaveNoti = ("%s has quit the server" % self.name)
		sendAll(leaveNoti, True)
		self.socket.close()
		index = getUserIndex(self.name)
		users.pop(index)
		self.runs = False
	def handleCommand(self, command):
		if (command == "!quit"):
			self.quit()
	def handleMessage(self, msg):
		global usercommands
		global message
		if (msg in usercommands):
			self.handleCommand(msg)
		else:
			message = ("%s: %s" % (self.name.upper(), msg))
			for x in users:
				if(x == self):
					continue
				else:
					x.socket.send(message.encode('ascii'))
	
	def run(self):
		global running
		global message
		global userNum
		global users
		print("Single listener for %s is set up" % self.address)
		self.changeName()
		while (running and self.runs):
			gotMsg = self.socket.recv(1024)
			msg = str(gotMsg.decode('ascii'))
			self.handleMessage(msg)

#connectionThread takes care of new connections, and adds new users to the users list
class connectionThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Connections thread initialized.\n")
		global userNum
		global running
		global nextID
		while running:			
			clientsocket,addr = serversocket.accept()
			user = chatUser(nextID, "", str(addr[0]), clientsocket)
			userNum += 1
			nextID += 1
			print("Got a connection from %s, total users: %d" % ( user.address, userNum))
			msg = "*** Welcome to the server! Please enter your name: ***"
			clientsocket.send(msg.encode('ascii'))
			users.append(user)
			users[(len(users)-1)].start()
						
#commandThread is processing the server terminal commands
class commandThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Command thread initialized.")
		global command
		global running
		while running:
			time.sleep(1)
			command = input("")
			if (command == "!users"):
				listOfUsers()
				continue
			if (command == "!sendall"):
				msg = input("Send to all users: ")
				noti = input("Notification? ")
				sendAll(msg, noti)
				continue
			else:
				print("Unknown command")
				continue

#prints the list of users				
def listOfUsers():
	print("ID | Name | Address")
	for x in users:
		print(x.id, x.name, x.address)
	print()
def sendAll(message, n):
	if(n=="1" or n=="y" or n==True or n=="true" or n=="yes"):
		msg = ("* %s *" % message)
	else:
		msg = ("SysOp: %s" % message)
	for x in users:
		x.socket.send(msg.encode('ascii'))
	print("%s  -- sent to all" % msg) 
	msg = ""
def getUserIndex(name):
	for x in users:
		if(x.name == name):
			return users.index(x)
				
users = [] #array for single listeners
usercommands = ["!quit"]
nextID = 0
userNum = 0
running = True
command = ""
message = ""

makeConnection()
comThread = commandThread()
comThread.start()
conThread = connectionThread()
conThread.start()

#dummy = input("Exit with enter")