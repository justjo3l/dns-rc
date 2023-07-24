from dataclasses import dataclass
import dataclasses
import struct

@dataclass
class DNSRecord:
    name: bytes
    type_: int
    class_: int
    ttl: int
    data: bytes

    def getName(self):
        return self.name