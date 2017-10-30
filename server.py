import socket

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

makeConnection()
#doing stuff
while True:
	clientsocket,addr = serversocket.accept()      
	print("Got a connection from %s" % str(addr[0]))
	msg = 'Thank you for connecting'+ "\r\n"
	clientsocket.send(msg.encode('ascii'))
	clientsocket.close()
#doing stuff ends here