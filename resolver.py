import sys
from socket import *
from dnsQuery import *
from decoder import *

TYPE_A = 1
TYPE_NS = 2

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

def send_query(address, name, record_type):
    query = build_query(name, record_type)
    temp_query_socket = socket(AF_INET, SOCK_DGRAM)
    temp_query_socket.sendto(query, (address, 53))

    data, _ = temp_query_socket.recvfrom(512)
    return decode_packet(data)

def get_answer(packet):
    answers = []

    for x in packet.answers:
        if x.type_ == TYPE_A:
            answers.append(x.data)

    return answers

def get_nameserver_ip(packet):
    for x in packet.additionals:
        if x.type_ == TYPE_A:
            return x.data

def get_nameserver(packet):
    for x in packet.authorities:
        if x.type_ == TYPE_NS:
            return x.data.decode("utf-8")

def resolve(name, record_type):
    addresses = parse_root_file('named.root')
    name_server = list(addresses.values())[0]
    while True:
        print(f"Querying {name_server} for {name}")
        response = send_query(name_server, name, record_type)
        if ips := get_answer(response):
            is_truncated = response.getTruncated()
            is_authoritative = response.getAuthoritative()
            return [ips, is_truncated, is_authoritative]
        elif nsIP := get_nameserver_ip(response):
            name_server = nsIP
        elif ns_domain := get_nameserver(response):
            name_server = resolve(ns_domain, TYPE_A)[0][0]
        else:
            raise Exception("SOMETHING WENT WRONG")

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

    receive_data = conn.recv(1024).decode()

    print("Received from client: ", receive_data)

    address = receive_data
    
    resolve_results = resolve(address, TYPE_A)

    output = "IPs: "

    for ip in resolve_results[0]:
        output += f"{ip}\n"

    output += f"Truncated: {resolve_results[1]}\n"
    output += f"Authoritative: {resolve_results[2]}"
    
    conn.send(output.encode())

    conn.close()
    udp_resolver_socket.close()

if __name__ == "__main__":
    main()