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
			try:
				data = input("")
				time.sleep(1)
			except UnicodeEncodeError:
				print("Please use only Unicode characters!")

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
				try:
					serversocket.send(data.encode('ascii'))
					data = ""
				except UnicodeEncodeError:
					print("Please use only Unicode characters!")
					data = ""
				except ConnectionResetError:
					print("Connection to the server aborted. Press a key to continue.")
					running = False
				
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
				print("Connection to the server closed. Press a key to continue.")
				running = False
			except ConnectionAbortedError:
				print("Connection to the server aborted.")
				running = False
			
				
def toBool(value):
	if value in trueSins:
		return True
	return False
def makeConnection():
	global serversocket
	global host
	global port
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#print("Socket created")
	host = input("Please enter the IP you would like to connect to: ")
	port = int(input("The port you would like to use: "))
	serversocket.connect((host,port))
	print("Connected to %s \n" % str((host,port)))
def closeConnection():
	serversocket.close()
def trimSettings():
	settings[0] = toBool(settings[0][14:-1])
	settings[1] = settings[1][10:-1]
	settings[2] = settings[2][12:-1]
	settings[3] = toBool(settings[3][10:])
def initSettings():
	cfgFile = open("cconfig.cfg", "r")
	line = "empty"
	while (line != ""):
		line = cfgFile.readline()
		settings.append(line)
	cfgFile.close()
	settings.pop()
	trimSettings()
	for x in settings:
		print("Value: %s, Type: %s" % (x, type(x)))
		

trueSins = ["True","true","1"]
data = ""
running = True
settings = []

makeConnection()
initSettings()
processTh = processThread()
listenTh = listenThread()
commandTh = commandThread()
processTh.start()
listenTh.start()
commandTh.start()
processTh.join()
listenTh.join()
commandTh.join()
closeConnection()

dummy = input("Exit with enter")