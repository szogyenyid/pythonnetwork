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
class singleListen(threading.Thread):
	def __init__(self, id, name, address, socket):
		threading.Thread.__init__(self)
		self.id = id
		self.name = name
		self.address = address
		self.socket = socket
	def run(self):
		global running
		global message
		global userNum
		global listens
		clientsocket = self.socket
		print("SingleListen for %s is set up" % self.address)
		#getName
		msg = clientsocket.recv(1024)
		newName = str(msg.decode('ascii'))
		self.name = newName
		for x in listens:
			if (self.id == x.id):
				x.setName(newName)
				continue
		print("%s is now known as %s" % (self.address, newName))
		joinNoti = ("%s connected to the server" %newName)
		sendAll(joinNoti, True)
		while running:
			msg = clientsocket.recv(1024)
			if (str(msg.decode('ascii')) == "!quit"):
				#Some more handling
				msg = "*** Goodbye, dear user! :') ***"
				clientsocket.send(msg.encode('ascii'))
				userNum = userNum-1
				nextID = self.id
				print("%s has quit, deleted his message listener and user" % newName)
				leaveNoti = ("%s has quit the server" % newName)
				sendAll(leaveNoti, True)
				index = getUserIndex(newName)
				listens[index].socket.close()
				listens.pop(index)
				break
			else:
				message = ("%s: %s" % (self.name.upper(), str(msg.decode('ascii'))))
				for x in listens:
					if(message == ""):
						break
					if(x.id == self.id):
						continue
					else:
						x.socket.send(message.encode('ascii'))
				message = ""
				continue

#connectionThread takes care of new connections, and adds new users to the users list
class connectionThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Connections thread initialized.")
		global userNum
		global running
		global nextID
		while running:			
			clientsocket,addr = serversocket.accept()
			user = singleListen(nextID, "", str(addr[0]), clientsocket)
			userNum += 1
			nextID += 1
			print("Got a connection from %s, total users: %d" % ( user.address, userNum))
			msg = "*** Welcome to the server! Please enter your name: ***"
			clientsocket.send(msg.encode('ascii'))
			listens.append(user)
			listens[(len(listens)-1)].start()
			
					
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
	for x in listens:
		print(x.id, x.name, x.address)
	print()
def sendAll(message, n):
	if(n=="1" or n=="y" or n==True or n=="true" or n=="yes"):
		msg = ("* %s *" % message)
	else:
		msg = ("SysOp: %s" % message)
	for x in listens:
		x.socket.send(msg.encode('ascii'))
	print("%s  -- sent to all" % msg) 
	msg = ""
def getUserIndex(name):
	for x in listens:
		if(x.name == name):
			return listens.index(x)
				
listens = [] #array for single listeners
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