import socket
import threading
import time

class commandThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global data
		global running
		while running:
			data = input("")
			time.sleep(1)
		#print("Command thread terminated")

class processThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global data
		global running
		while running:
			if (data == ""):
				time.sleep(0.5)
				continue
			if (data.lower() == "!quit"):
				serversocket.send(data.lower().encode('ascii'))
				data = ""
				print("Thanks for using me!")
				running = False
				break
			else:
				serversocket.send(data.encode('ascii'))
				data = ""
		#print("Process thread terminated")
				
class listenThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		global running
		while running:
			try:
				msg = serversocket.recv(1024)
				if (len(msg.decode('ascii')) > 0):
					print (msg.decode('ascii'))
					msg = ""
			except ConnectionResetError:
				print("Connection to the server aborted. Press a key to continue.")
				running = False
		#print("Listen thread terminated")
			
				
def makeConnection():
	global serversocket
	global host
	global port
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created")
	host = input("Please enter the IP you would like to connect to: ")
	port = int(input("The port you would like to use: "))
	serversocket.connect((host,port))
	print("Connected to %s \n" % str((host,port)))
def closeConnection():
	serversocket.close()
	
makeConnection()
#doing stuff
data = ""
running = True
processTh = processThread()
listenTh = listenThread()
commandTh = commandThread()
processTh.start()
listenTh.start()
commandTh.start()
processTh.join()
listenTh.join()
commandTh.join()
#doing stuff ends
closeConnection()
dummy = input("Exit with enter")