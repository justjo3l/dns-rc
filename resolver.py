import sys
from socket import *

if (len(sys.argv) < 2):
    print("Error: Invalid number of arguments")
    print("Usage: python resolver.py <resolver_port>")
    sys.exit()

ip = "127.0.0.1"
port = sys.argv[1]
buffer_size = 1024

print("Port: " + port)

udp_resolver_socket = socket(AF_INET, SOCK_DGRAM)
udp_resolver_socket.bind((ip, int(port)))

print("UDP Resolver active and listening!")

while(True):
    receive_data = udp_resolver_socket.recvfrom(buffer_size)
    message = receive_data[0]
    address = receive_data[1]
    print("Client message: " + str(message))
    print("Client address: " + str(address))
    udp_resolver_socket.sendto(str.encode("Message received!"), address)