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
			addresses.append(addr[0])
			users = users+1
			print("Got a connection from %s, total users: %d" % ( str(addr[0]), users))
			msg = "***Welcome to the server! Your next message will be your username.***"
			clientsocket.send(msg.encode('ascii'))
			msg = clientsocket.recv(1024)
			usernames.append(msg.decode('ascii'))
			print("%s is now known as %s" % (str(addr[0]), usernames[(users-1)]))
			
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
		while running:
			
		

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