from dataclasses import dataclass
import dataclasses
import struct
from typing import List
from dnsHeader import *
from dnsQuestion import *
from dnsRecord import *

@dataclass
class DNSPacket:
    header: DNSHeader
    questions: List[DNSQuestion]
    answers: List[DNSRecord]
    authorities: List[DNSRecord]
    additionals: List[DNSRecord]