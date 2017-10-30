import socket
import threading
import time

def makeConnection():
	global serversocket
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created")
	host = input("Please enter your ip address: ")
	port = int(input("The port you would like to use: "))
	serversocket.bind((host, port))
	print("Socket bound to %s" % str((host,port)))
	serversocket.listen(5)
	print("Listener initialized")

class chatUser():
	def __init__(self, name, address, socket):
		self.name = name
		self.address = address
		self.socket = socket
	def setName(self, newName):
		self.name = newName
	
class singleListen(threading.Thread):
	def __init__(self, name, address, socket):
		threading.Thread.__init__(self)
		self.name = name
		self.address = address
		self.socket = socket
	def run(self):
		print("SingleListen for %s is set up" % self.name)
		global running
		global message
		clientsocket = self.socket
		while running:
			msg = clientsocket.recv(1024)
			message = str(msg.decode('ascii'))
			if (message == "!quit"):
				print("I should handle when someone quits :(")
				continue
			else:
				continue

#connectionThread takes care of new connections, and adds new users to the users list (maybe DONE)
class connectionThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Connections thread initialized.")
		global users
		global userNum
		global running
		while running:
			clientsocket,addr = serversocket.accept()
			user = chatUser("",str(addr[0]),clientsocket)
			userNum = userNum+1
			print("Got a connection from %s, total users: %d" % ( user.address, userNum))
			msg = "***Welcome to the server! Your next message will be your username.***"
			clientsocket.send(msg.encode('ascii'))
			msg = clientsocket.recv(1024)
			newName = str(msg.decode('ascii'))
			user.setName(newName)
			print("%s is now known as %s" % (user.address, user.name))
			users.append(user)
			listens.append(singleListen(user.name, user.address, user.socket))
			listens[(userNum-1)].start()
			
#processThread says goodbye to a user, manages quits, and transmits messages to other users
class processThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Processing thread initialized.")

					
#commandThread is processing the server terminal commands (Done for now, new functions coming)
class commandThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Command thread initialized.")
		global command
		global running
		while running:
			command = input("")
			time.sleep(1)
		
listens = []
users = []
userNum = 0
running = True
command = ""
message = ""
#
#Have to do:
#Lisiten to new messages -> listenThread
#Send new messages to everyone but sender -> processThread
#change username -> processThread
#when msg is "!quit" send back a goodbye message
#
#doing stuff
makeConnection()

comThread = commandThread()
comThread.start()
conThread = connectionThread()
conThread.start()
#doing stuff ends here
#dummy = input("Exit with enter")