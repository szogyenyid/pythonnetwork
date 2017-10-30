import socket
import threading

def makeConnection():
	global serversocket
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created")
	#host = input("Please enter your ip address: ")
	port = int(input("The port you would like to use: "))
	serversocket.bind(('localhost', port))
	print("Socket bound to %s" % str(('localhost',port)))
	serversocket.listen(5)
	print("Listener initialized")

class connectionThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		print("Connections thread initialized.")
	
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


	

makeConnection()
#doing stuff
#Have to do:
#Listen to new connections, and manage users -> connectionThread
#Get username
#Lisiten to new messages -> listenThread
#Send new messages to everyone but sender -> processThread
#change username -> processThread
#
running = True
while running:
	clientsocket,addr = serversocket.accept()      
	print("Got a connection from %s" % str(addr[0]))
	msg = 'SERVER: Thank you for connecting'+ "\r\n"
	clientsocket.send(msg.encode('ascii'))
	while True:
		msg = clientsocket.recv(1024)
		clientsocket.send(msg)
		msg = ''
#doing stuff ends here
dummy = input("Quit")