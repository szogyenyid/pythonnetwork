import socket

def makeConnection():
	global clientsocket
	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print("Socket created")
	host = input("Please enter the IP you would like to connect to: ")
	port = int(input("The port you would like to use: "))
	clientsocket.connect((host,port))
	print("Connected to %s" % str((host,port)))
	
def closeConnection():
	clientsocket.close()
	
makeConnection()
#doing stuff
msg = clientsocket.recv(1024)
print ("Message from server: " + msg.decode('ascii'))
#doing stuff ends
closeConnection()
dummy = input("Quit")