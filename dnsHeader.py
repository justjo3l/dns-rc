from dataclasses import dataclass

@dataclass
class DNSHeader:
    id: int
    flags: int
    num_questions: int = 0
    num_answers: int = 0
    num_authorities: int = 0
    num_additionals: int = 0

    def getTruncated(self):
        is_truncated = bool(self.flags & 0b00100000)
        return is_truncated
    
    def getAuthoritative(self):
        is_authoritative = bool(self.flags & 0b00010000)
        return is_authoritative
    
    def getResponseCode(self):
        response_code = self.flags & 0b00001111
        return response_code