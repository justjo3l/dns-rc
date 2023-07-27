from dataclasses import dataclass
import dataclasses
import struct

def header_to_bytes(header):
    fields = dataclasses.astuple(header)
    return struct.pack("!HHHHHH", *fields)

def question_to_bytes(question):
    return question.name + struct.pack("!HH", question.type_, question.class_)

def encode_dns_name(name):
    encoded = b""
    for segment in name.encode("ascii").split(b"."):
        encoded += bytes([len(segment)]) + segment
    return encoded + b"\x00"