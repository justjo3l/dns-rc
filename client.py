import sys
from socket import *

timeout_length = 5

if (len(sys.argv) < 4):
    print("Error: Invalid number of arguments")
    print("Usage: python client.py <resolver_ip> <resolver_port> <name> [timeout=5]")
    sys.exit()

ip = sys.argv[1]
port = sys.argv[2]
name_server = sys.argv[3]
if (len(sys.argv) == 5):
    timeout_length = sys.argv[4]
buffer_size = 1024

print("IP Address: " + ip)
print("Port: " + port)
print("Name Server: " + name_server)

udp_client_socket = socket(AF_INET, SOCK_STREAM)
udp_client_socket.settimeout(timeout_length)
udp_client_socket.connect((ip, int(port)))
try:
    udp_client_socket.send(str.encode(name_server))

    receive_data = udp_client_socket.recv(1024).decode()
    print("Received from server: ", receive_data)
except (udp_client_socket.timeout):
    print("Resolver did not respond")
finally:
    udp_client_socket.close()