from dataclasses import dataclass
from typing import List
from dnsHeader import *
from dnsQuestion import *
from dnsRecord import *
from decoder import *

def ip_to_string(ip):
    return ".".join([str(x) for x in ip])

@dataclass
class DNSPacket:
    header: DNSHeader
    questions: List[DNSQuestion]
    answers: List[DNSRecord]
    authorities: List[DNSRecord]
    additionals: List[DNSRecord]

    def getTruncated(self):
        return self.header.getTruncated()

    def getAuthoritative(self):
        return self.header.getAuthoritative()

def getAddresses(packet):
    addresses = []

    for additional in packet.additionals:
        address = ip_to_string(additional.data)
        if (address.count('.') <= 3):
            addresses.append(address)

    return addresses

def getNames(packet):
    names = []

    for authority in packet.authorities:
        names.append(authority.getName())

    return names