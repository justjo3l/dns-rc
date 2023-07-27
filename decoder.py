from dataclasses import dataclass
import struct
from dnsHeader import *
from dnsQuestion import *
from dnsRecord import *
from dnsPacket import *
from io import BytesIO


TYPE_A = 1
TYPE_NS = 2

def decode_headers(reader):
    items = struct.unpack("!HHHHHH", reader.read(12))
    return DNSHeader(*items)

def decode_name(reader):
    parts = []
    while (length := reader.read(1)[0]) != 0:
        if length & 0b1100_0000:
            parts.append(decode_compressed_name(length, reader))
            break
        else:
            parts.append(reader.read(length))
    return b".".join(parts)

def decode_compressed_name(length, reader):
    pointer_bytes = bytes([length & 0b0011_1111]) + reader.read(1)
    pointer = struct.unpack("!H", pointer_bytes)[0]
    current_pos = reader.tell()
    reader.seek(pointer)
    result = decode_name(reader)
    reader.seek(current_pos)
    return result

def decode_question(reader):
    name = decode_name(reader)
    data = reader.read(4)
    type_, class_ = struct.unpack("!HH", data)
    return DNSQuestion(name, type_, class_)

def decode_record(reader):
    name = decode_name(reader)
    data = reader.read(10)
    type_, class_, ttl, data_len = struct.unpack("!HHIH", data)
    if type_ == TYPE_NS:
        data = decode_name(reader)
    elif type_ == TYPE_A:
        data = ip_to_string(reader.read(data_len))
    else:
        data = reader.read(data_len)
    return DNSRecord(name, type_, class_, ttl, data)

def print_decoded_response(response):
    reader = BytesIO(response)
    print(decode_record(reader))

def decode_packet(data):
    reader = BytesIO(data)
    headers = decode_headers(reader)
    questions = [decode_question(reader) for _ in range(headers.num_questions)]
    answers = [decode_record(reader) for _ in range(headers.num_answers)]
    authorities = [decode_record(reader) for _ in range(headers.num_authorities)]
    additionals = [decode_record(reader) for _ in range(headers.num_additionals)]

    return DNSPacket(headers, questions, answers, authorities, additionals)