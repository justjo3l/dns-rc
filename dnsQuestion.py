from dataclasses import dataclass

@dataclass
class DNSQuestion:
    name: bytes
    type_: int
    class_: int