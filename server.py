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
		try:
			if(self.name == ""):
				justConnected = True
			else:
				justConnected = False
				oldName = self.name
				msg = "Please enter your new name:"
				self.socket.send(msg.encode('ascii'))
			msg = self.socket.recv(1024)
			newName = str(msg.decode('ascii'))
			if(nameIsValid(newName)):
				self.name = newName
				print("%s is now known as %s\n" % (self.address, newName))
				if(justConnected):
					joinNoti = ("%s connected to the server" %newName)
				else:
					joinNoti = ("%s is now known as %s" % (oldName, newName))
				sendAll(joinNoti, True)
			else:
				msg = "Sorry, the name you chose is already taken. \nPlease enter another name: "
				self.socket.send(msg.encode('ascii'))
				self.changeName()
		except ConnectionResetError:
			leaveNoti = ("%s forced to quit the client." % self.name)
			print(leaveNoti)
			sendAllBut(self, leaveNoti, True)
			self.kill()
	def kill(self):
		global userNum
		userNum -= 1
		print("%s has quit, deleted his message listener and user" % self.name)
		self.socket.close()
		index = getUserIndex(self.name)
		users.pop(index)
		self.runs = False
	def kick(self):
		leaveNoti = ("%s has quit the server" % self.name)
		sendAllBut(self, leaveNoti, True)
		msg = "*** You have been kicked from the server! ***"
		self.socket.send(msg.encode('ascii'))
		self.kill()
	def quit(self):
		leaveNoti = ("%s has quit the server" % self.name)
		sendAllBut(self, leaveNoti, True)
		msg = "*** Goodbye, dear user! :') ***"
		self.socket.send(msg.encode('ascii'))
		self.kill()
	def handleCommand(self, command):
		global users
		if (command == "!quit"):
			self.quit()
		if (command == "!name"):
			self.changeName()
		if (command == "!users"):
			msg = ""
			for x in users:
				msg += x.name
				msg += (", ")
			msg = msg[:-2]
			self.socket.send(msg.encode('ascii'))
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
			try:
				gotMsg = self.socket.recv(1024)
				msg = str(gotMsg.decode('ascii'))
				self.handleMessage(msg)
			except (ConnectionResetError):
				leaveNoti = ("%s forced to quit the client." % self.name)
				print(leaveNoti)
				sendAllBut(self, leaveNoti, True)
				self.kill()
			except (ConnectionAbortedError):
				if (self.isAlive()):
					print("Connection to %s aborted." % self.name)
					runs = False
				else:
					runs = False
					pass

#connectionThread takes care of new connections, and adds new users to the users list
class connectionThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.pswSucc = True
	def getPass(self, clientsocket):
		global password
		passPrompt = "The server requires a password to enter. Please enter it:"
		clientsocket.send(passPrompt.encode('ascii'))
		userPass = clientsocket.recv(1024)
		if (userPass.decode('ascii') != password):
			msg = "The password you entered is wrong."
			clientsocket.send(msg.encode('ascii'))
			self.pswSucc = False
	def run(self):
		print("Connections thread initialized.\n")
		global userNum
		global running
		global password
		global nextID
		while running:			
			clientsocket,addr = serversocket.accept()
			user = chatUser(nextID, "", str(addr[0]), clientsocket)
			if (password != ""):
				self.getPass(clientsocket)
			if (self.pswSucc):
				userNum += 1
				nextID += 1
				print("Got a connection from %s, total users: %d" % ( user.address, userNum))
				msg = "*** Welcome to the server! Please enter your name: ***"
				clientsocket.send(msg.encode('ascii'))
				users.append(user)
				users[(len(users)-1)].start()
			else:
				clientsocket.send("Authentication failed.".encode('ascii'))
				clientsocket.close()
				self.pswSucc = True

#commandThread is processing the server terminal commands
class commandThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def handleCommand(self, command):
		global servercommands
		global users
		global password
		if (command in servercommands):
			if(command == "!users"):
				listOfUsers()
			if(command == "!sendall"):
				msg = input("Send to all users: ")
				noti = input("Notification? ")
				sendAll(msg, noti)
			if(command == "!kick"):
				name = input("Who would you like to kick? ")
				kickIndex = getUserIndex(name)
				if (type(kickIndex) is int):
					users[kickIndex].kick()
				else:
					return
			if(command == "!setpass"):
				newPass = input("What would you like for new server password? ")
				password = newPass
				print("New password is set to \"%s\" \n" % password)
			if(command == "!shutdown"):
				secs = input("How many seconds would you like before shutting down? ")
				shutDown(secs)
		else:
			print("Unknown command")
	
	def run(self):
		print("Command thread initialized.")
		global command
		global running
		while running:
			time.sleep(1)
			command = input("")
			self.handleCommand(command)

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
def sendAllBut(user, message, n):
	if(n=="1" or n=="y" or n==True or n=="true" or n=="yes"):
		msg = ("* %s *" % message)
	else:
		msg = ("SysOp: %s" % message)
	for x in users:
		if (x == user):
			continue
		else:
			x.socket.send(msg.encode('ascii'))
	print("%s  -- sent to all" % msg) 
	msg = ""
def getUserIndex(name):
	for x in users:
		if(x.name.lower() == name.lower()):
			return users.index(x)
	for x in users:
		if(x.address == name):
			return users.index(x)
	print("No user found with this name or address.")
def nameIsValid(name):
	for x in users:
		if(x.name.lower() == name.lower()):
			return False
	return True
def killAll():
		for x in users:
			x.kill()
def shutDown(sec):
	msg = ("\nAttention!\nThe server will shut down in %s seconds! Please leave the server.\n" % str(sec))
	sendAll(msg, True)
	timeLeft = int(sec)
	
	while(timeLeft > 0):
		if (timeLeft>15):
			msg = ("Shutting down server in %s seconds." % timeLeft)
			sendAll(msg, True)
			time.sleep(15)
			timeLeft -= 15
		else:
			msg = ("Shutting down server in %s seconds." % timeLeft)
			sendAll(msg, True)
			time.sleep(timeLeft)
			timeLeft = 0
	killAll()
	print("Killed all connections.")
	running = False
	
users = [] #array for users

usercommands = ["!quit", "!name", "!users"]
usercomdesc = ["Disconnect from server,and quit the client.","Change username.","List of online users."]

servercommands = ["!users", "!sendall", "!kick", "!setpass", "!shutdown"]
servercomdesc = ["List of online users.","Send a message for all users.","Kick a user.","Set password for server.","Shut down the server."]

password = ""
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

conThread.join()
comThread.join()

dummy = input("Exit with enter")