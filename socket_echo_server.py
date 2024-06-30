# Group 21
# Algo Woolf (300267107)
# Kevin Luong (300232125)
# Nalan Kurnaz (300245521)

import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

##Then bind() is used to associate the socket with the server address. In this case, the address is localhost, referring to the current server, and the port number is 10000.

# Bind the socket to the port
server_address = ('localhost', 10800)
print( 'starting up on %s port %s' %server_address)
sock.bind(server_address)

##Calling listen() puts the socket into server mode, and accept() waits for an incoming connection.

# Listen for incoming connections
sock.listen(1)

##accept() 
# returns an open connection between the 
# server and client, along with the address 
# of the client. The connection is actually a 
# different socket on another port (assigned by the 
# kernel). Data is read from the connection with recv() and 
# transmitted with sendall().

def encodeHextoIP(hexAddr:str) -> str:
    #Split the hex address into two-character chunks
    hexPairs = [hexAddr[i:i+2] for i in range(0, len(hexAddr), 2)]

    #Convert each hex pair to decimal
    decimalPairs = [str(int(pair, 16)) for pair in hexPairs]

    #Join decimal values with dots
    decimalIP = ".".join(decimalPairs)

    return decimalIP

def hexToString(hex_str) -> str:
    #Split the hex value into groups of two
    #two hexadecimal characters represent one ascii character
    chars = [hex_str[i:i+2] for i in range(0, len(hex_str), 2)]

    #Convert each hex group to an ASCII char
    #hex -> decimal -> ascii
    string = "".join(chr(int(char, 16)) for char in chars)

    #since the encoded message may add null characters at the end of the message to make it divisible by 8,
    #slice up to the first null character to get the original string
    slice_index = string.find('\x00')
    string = string[:slice_index]
    return string

def onesComplement(hexValue:str) -> str:
    complement = int("FFFF", 16) - int(hexValue, 16)
    complement = hex(complement)[2:].zfill(4)
    return complement

def decodeMessage(message:str) -> str:
    
    #checksum verification and assigning each part will be done here
    words = []
    for i in range(0, len(received_packet), 4):
        words.append(received_packet[i:i+4])
    version = words[0][0]
    headerLen = words[0][1]
    typeOfService = words[0][2:4]
    sourceIP = encodeHextoIP("".join(words[6:8]))
    destinationIP = encodeHextoIP("".join(words[8:10]))
    received_checksum = words[5]
    message = "".join(words[10:])  
    totalLen = words[1]

    total = 0
    for word in words[:10]:
        total += int(word, 16)
    
    total = hex(total)[2:]

    if len(total) > 4:
        carry = total[:-4]
        total = total[-4:]
        total = int(total, 16) + int(carry, 16)
        total = hex(total)[2:].zfill(4)
    
    checking_checksum = onesComplement(total)

    if(checking_checksum == "0000"):
        decodedMessage = hexToString(message)
        server_output = (f"The data received from {sourceIP} is: {decodedMessage} " + "\n" +
                     f"The data has {len(message) * 4} bits or {len(message) // 2} bytes.\n"
                     f"The total length of the packet is {int(totalLen, 16)} bytes.\n"
                     "The verification of the checksum demonstrates that the packet received is correct.")
        print(server_output)  
        return decodedMessage
    else:
        output = "The verification of the checksum demonstrates that the packet received is corrupted. Packet discarded."
        print(output)
        return output   
    
connection_open = True

while connection_open:
    print('waiting for a connection')
    connection, client_address = sock.accept()
    print("Connection from ", client_address)
    received_packet = ""

    while True:
        try:
            connection.setblocking(0) #change the socket to non-blocking so that connection.recv() does not block
            #the program while waiting for data

            data = connection.recv(1024) #if buffer is empty, an error is thrown

            print('received:', data)
            received_packet += data.decode('utf-8')
            
            response = decodeMessage(received_packet)
            connection.sendall(response.encode('utf-8'))
        except:
            #if packets were received and an error is thrown that means that no more data is being transmitted
            if received_packet:
                print ('no more data from', client_address)
                connection_open = False #close the connection by ending the outer loop
                break #end the loop once there is no more data
            #no data received yet, so continue waiting for data to arrive
            else:
                continue

print("closing connection")
connection.close()