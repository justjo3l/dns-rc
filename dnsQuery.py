import random
from encoder import *
from dnsHeader import *
from dnsQuery import *
from dnsQuestion import *
from dataclasses import dataclass
import dataclasses

random.seed(1)

TYPE_A = 1
CLASS_IN = 1

def build_query(domain_name, record_type):
    name = encode_dns_name(domain_name)
    id = random.randint(0, 65535)
    RECURSION_DESIRED = 0 << 8
    header = DNSHeader(id=id, num_questions=1, flags=RECURSION_DESIRED)
    question = DNSQuestion(name=name, type_=record_type, class_=CLASS_IN)
    return header_to_bytes(header) + question_to_bytes(question)

# def main():
#     print(build_query("www.google.com", 1))

# if __name__ == "__main__":
#     main()