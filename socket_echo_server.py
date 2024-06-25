import socket
import sys
import binascii

# def hex_to_string(hex_str):
# ## convert hex string to binary data -> binary data to string
#     return binascii.unhexlify(hex_str).decode('utf-8')

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
        output = (f"The data received from {sourceIP} is: {hexToString(message)}\n"
                  f"The data has {len(message) * 4} bits or {len(message) // 2} bytes.\n"
                  f"The total length of the packet is {int(totalLen, 16)} bytes.\n"
                  "The verification of the checksum demonstrates that the packet received is correct.")
        print(output)
        return output
    else:
        output = "The verification of the checksum demonstrates that the packet received is corrupted. Packet discarded."
        print(output)
        return output   
    

while True:
    print ('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print("Connection from ", client_address)
        received_packet = ""
        # print("checkpoint 1")
        while True:
            data = connection.recv(1024)
            # print("checkpoint 2")
            if data:
                print ('received :', data)
                received_packet += data.decode('utf-8')
            else:
                print ('no more data from', client_address)
                break
        response = decodeMessage(received_packet)
        connection.sendall(response.encode('utf-8'))
    finally:
        connection.close()




    
    # try:
    #     print  ('connection from ', client_address)
    #     received_packet = received_packet.decode('utf-8')
         
    #     # here we choose the size of the buffer e.g. 100 
    #      # Receive the data in small chunks and retransmit it
    #     while True:
    #         data = connection.recv(1024)
    #         print ('received :' , data)
    #         if data:
               
    #             received_string = hexToString(hex_data)
    #             print ('received string: ', received_string)
    #             print ('sending data back to the client')
    #             connection.sendall(data)
    #         else:
    #             print ('no more data from', client_address)
    #             break
            
    # finally:
    #     # Clean up the connection
    #     connection.close()


