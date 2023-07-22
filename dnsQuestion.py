from dataclasses import dataclass
import dataclasses
import struct

@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int