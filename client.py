import sys
from socket import *

if (len(sys.argv) < 4):
    print("Error: Invalid number of arguments")
    print("Usage: python client.py <resolver_ip> <resolver_port> <name>")
    sys.exit()

ip = sys.argv[1]
port = sys.argv[2]
name_server = sys.argv[3]
buffer_size = 1024

print("IP Address: " + ip)
print("Port: " + port)
print("Name Server: " + name_server)

udp_client_socket = socket(AF_INET, SOCK_DGRAM)

udp_client_socket.sendto(str.encode(name_server), (ip, int(port)))

resolver_response = udp_client_socket.recvfrom(buffer_size)

print("Resolver response: " + resolver_response[0])