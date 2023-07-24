from dataclasses import dataclass
import dataclasses
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

def print_old_decoded_response(response):
    header_id = int.from_bytes(response[0:2], byteorder='big')
    header_flags = int.from_bytes(response[2:4], byteorder='big')
    header_questions = int.from_bytes(response[4:6], byteorder='big')
    header_answer_rrs = int.from_bytes(response[6:8], byteorder='big')
    header_authority_rrs = int.from_bytes(response[8:10], byteorder='big')
    header_additional_rrs = int.from_bytes(response[10:12], byteorder='big')

    response_code = header_flags & 0b00001111
    is_authoritative = bool(header_flags & 0b00010000)
    is_truncated = bool(header_flags & 0b00100000)
    is_recursion_desired = bool(header_flags & 0b10000000)
    is_recursion_available = bool(header_flags & 0b01000000)

    question_offset = 12
    question_name = ''
    while True:
        label_length = response[question_offset]
        if label_length == 0:
            break
        question_name += response[question_offset+1:question_offset+1+label_length].decode('utf-8') + "."
        question_offset += label_length + 1
    question_name = question_name[:-1]

    question_type = response[question_offset+1:question_offset+3]
    question_class = response[question_offset+3:question_offset+5]
    
    answer_offset = question_offset + 5
    answer_name = question_name
    answer_type = response[answer_offset+1:answer_offset+3]
    answer_class = response[answer_offset+3:answer_offset+5]
    answer_ttl = int.from_bytes(response[answer_offset+5:answer_offset+9], byteorder='big')
    answer_data_length = int.from_bytes(response[answer_offset+9:answer_offset+11], byteorder='big')
    answer_data = '.'.join(str(byte) for byte in response[answer_offset+12:answer_offset+11+answer_data_length])

    print("Query: ", question_name)
    print("Type: ", question_type)
    print("Class: ", question_class)
    print("Answer: ", answer_data)