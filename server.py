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
	def setName(newName):
		self.name = newName
	
class connectionThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Connections thread initialized.")
		global usernames
		global addresses
		global users
		global running
		while running:
			clientsocket,addr = serversocket.accept()
			user = chatUser("",str(addr[0]),clientsocket)
			users = users+1
			print("Got a connection from %s, total users: %d" % ( user.address, users))
			msg = "***Welcome to the server! Your next message will be your username.***"
			clientsocket.send(msg.encode('ascii'))
			msg = clientsocket.recv(1024)
			newName = str(msg.decode('ascii'))
			user.setName(newName)
			print("%s is now known as %s" % (user.address, user.name))
			users.append(user)
			
class processThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Processing thread initialized.")
	
class listenThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Listening thread initialized.")
		global running
			
		

class commandThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Command thread initialized.")
		global data
		global running
		while running:
			data = input("")
			time.sleep(1)
		
users = []
users = 0
running = True
data = ""
#
#Have to do:
#Listen to new connections, and manage users -> connectionThread
#Get username
#Lisiten to new messages -> listenThread
#Send new messages to everyone but sender -> processThread
#change username -> processThread
#
#doing stuff
makeConnection()

comThread = commandThread()
comThread.start()
conThread = connectionThread()
conThread.start()
#doing stuff ends here
#dummy = input("Exit with enter")