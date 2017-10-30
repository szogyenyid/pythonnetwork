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
	def __init__(self, id, name, address, socket):
		self.id = id
		self.name = name
		self.address = address
		self.socket = socket
	def setName(self, newName):
		self.name = newName
	
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
		clientsocket = self.socket
		print("SingleListen for %s is set up" % self.name)
		while running:
			msg = clientsocket.recv(1024)
			message = str(msg.decode('ascii'))
			if (message == "!quit"):
				print("I should handle when someone quits :(") #TODO
				userNum = userNum-1
				
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
		global nextID
		while running:
			clientsocket,addr = serversocket.accept()
			user = chatUser(nextID, "", str(addr[0]),clientsocket)
			nextID = nextID+1
			print("Got a connection from %s, total users: %d" % ( user.address, userNum))
			msg = "***Welcome to the server! Your next message will be your username.***"
			clientsocket.send(msg.encode('ascii'))
			msg = clientsocket.recv(1024)
			newName = str(msg.decode('ascii'))
			user.setName(newName)
			print("%s is now known as %s" % (user.address, user.name))
			users.append(user)
			listens.append(singleListen(user.id, user.name, user.address, user.socket))
			listens[(nextID-1)].start()
			
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
			if (command == "!users"):
				listOfUsers()
				continue
			else:
				continue
		
def listOfUsers():
	print("ID | Name | Address")
	for x in users:
		print(x.id, x.name, x.address)
		
		
listens = []
users = []
nextID = 0
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
#quit = empty element of array, do not delete it
#maximum number of users
#doing stuff
makeConnection()

comThread = commandThread()
comThread.start()
conThread = connectionThread()
conThread.start()
#doing stuff ends here
#dummy = input("Exit with enter")