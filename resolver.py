import sys
from socket import *
from dnsQuery import *
from decoder import *

def parse_root_file(file_name):
    f = open(file_name, 'r+')
    file_content = f.readlines()

    addresses = dict()

    for line in file_content:
        line = line.strip()
        if ('  A  ' in line):
            elements = line.split()
            addresses[elements[0].strip()] = elements[3].strip()

    return addresses

def print_parsed(addresses):
    for key, value in addresses.items():
        print(key + " - " + value)

def main():

    if (len(sys.argv) < 2):
        print("Error: Invalid number of arguments")
        print("Usage: python resolver.py <resolver_port>")
        sys.exit()

    ip = "127.0.0.1"
    port = sys.argv[1]

    udp_resolver_socket = socket(AF_INET, SOCK_STREAM)
    udp_resolver_socket.bind((ip, int(port)))
    udp_resolver_socket.listen(1)

    print(f"UDP Resolver active and listening on port {port}!")

    conn, address = udp_resolver_socket.accept()
    print("Connection from ", address)

    addresses = parse_root_file('named.root')
    print_parsed(addresses)

    receive_data = conn.recv(1024).decode()

    print("Received from client: ", receive_data)

    query_socket = socket(AF_INET, SOCK_DGRAM)
    address = receive_data
    print("Client address: " + str(address))

    query = build_query(address, 1)

    # while True:
    for key, value in addresses.items():
        query_socket.sendto(query, (value, 53))
        response, _ = query_socket.recvfrom(512)
        print(f"{key}:")
        packet = decode_packet(response)
        print(getAddresses(packet))
    
    conn.send("Hi".encode())

    conn.close()
    udp_resolver_socket.close()

if __name__ == "__main__":
    main()