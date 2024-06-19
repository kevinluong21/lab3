import socket
import sys

# # Create a TCP/IP socket
Client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # Connect the socket to the port where the server is listening
# server_address = ('localhost', 10800)
# print ('connecting to ', server_address)
# Client_socket.connect(server_address)

##After the connection is established, data can be sent through the socket with sendall() and received with recv(), just as in the server.

def encodeIPtoHex(ipAddr:str):
    ipAddr = ipAddr.split(".") #split by the periods in the IP address
    temp = ""
    for octet in ipAddr:
        octet = hex(int(octet))[2:] #hex appends "0x" to the start, so we need to slice to keep the values after "0x"
        octet = octet.zfill(2) #hex may drop leading zeroes, so pad the octet with leading zeroes to get a string of length 2
        temp = temp + octet
    return temp

def onesComplement(hexValue:str):
    complement = int("FFFF", 16) - int(hexValue, 16)
    complement = hex(complement)[2:].zfill(4)
    return complement

try:
    # Send data
    # message = b'This is a massage from hamzah.  It will be repeated.'
    # you can enter the massage from keyboard this way. instead of the fixed massage above
    value = input("Please enter the message you want to be echoed:\n")
    message = value.encode('utf-8').hex() #message is encoded to ASCII/hex

    version = "4"
    headerLen = "5"
    typeOfService = "00"

    # A byte is 8 bits, so if each hex digit is 4 bits, then the total payload length in bytes is the length / 2
    payloadLen = len(message) / 2
    totalLen = (int(headerLen) * 4) + payloadLen #each digit represents 4 bits
    totalLen = hex(int(totalLen))[2:]
    totalLen = totalLen.zfill(4)

    identification = "1c46" #NOTE: must be auto-generated to be unique to each packet

    flags = "40"
    fragmentOffset = "00"

    timeToLive = "40"
    protocol = "06"

    sourceIP = socket.gethostbyname(socket.gethostname())
    sourceIP = "192.168.0.3"
    sourceIP = encodeIPtoHex(sourceIP)

    serverIP = socket.gethostbyname("localhost")
    serverIP = "192.168.0.1"
    serverIP = encodeIPtoHex(serverIP)

    temp = version + headerLen + typeOfService + totalLen + identification + flags + fragmentOffset + timeToLive + protocol + sourceIP + serverIP

    words = [] #stores each 4-byte word in the header
    for i in range(0, len(temp), 4):
        words.append(temp[i:i + 4])

    total = 0
    for i in range(len(words)):
        total = total + int(words[i], 16)

    total = hex(total)[2:]
    total = total.zfill(4)

    # if there is a carry, add it back to the sum
    if len(total) > 4:
        carry = total[:-4] #the carry is all values in front of the four digits 
        total = total[-4:] #take the last 4 digits
        total = int(total, 16) + int(carry, 16)
        #convert back to hexadecimal
        total = hex(total)[2:].zfill(4)

    checksum = onesComplement(total)

    packet = version + headerLen + typeOfService + totalLen + identification + flags + fragmentOffset + timeToLive + protocol + checksum + sourceIP + serverIP + message + "00"

    #if the packet length is NOT divisible by 4, we need to pad with trailing zeroes so that the entire packet is divisible by 4
    if len(packet) % 4 != 0:
        packet = packet.ljust(len(packet) + (4 - len(packet) % 4), "0")
    
    #testing!!!
    # words = [] #stores each 4-byte word in the header
    # for i in range(0, len(packet), 4):
    #     words.append(packet[i:i + 4])

    # print(words)

    # print( 'sending : ' ,  message)
    # Client_socket.sendall(message)

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    
    
    # here we choose the size of the buffer e.g. 100 
    # while amount_received < amount_expected:
    #     data = Client_socket.recv(100)
    #     amount_received += len(data)
    #     print ('received :' , data) 

finally:
    print('closing socket')
    # Client_socket.close()