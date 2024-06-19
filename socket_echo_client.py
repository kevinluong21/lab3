import socket
import sys

# Create a TCP/IP socket
Client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10800)
print ('connecting to ', server_address)
Client_socket.connect(server_address)

##After the connection is established, data can be sent through the socket with sendall() and received with recv(), just as in the server.

try:
    
    # Send data
    # message = b'This is a massage from hamzah.  It will be repeated.'
    # you can enter the massage from keyboard this way. instead of the fixed massage above
    value = input("Please enter  the massage you want to be echoed:\n")
    message = value.encode('utf-8')
    print( 'sending : ' ,  message)
    Client_socket.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    
    
    # here we choose the size of the buffer e.g. 100 
    while amount_received < amount_expected:
        data = Client_socket.recv(100)
        amount_received += len(data)
        print ('received :' , data) 

finally:
    print('closing socket')
    Client_socket.close()