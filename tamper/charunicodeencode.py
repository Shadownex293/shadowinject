from .base import TamperBase

class CharUnicodeEncode(TamperBase):
    def __init__(self):
        self.name = "charunicodeencode"
        
    def tamper(self, payload):
        # Encode characters as %uXXXX
        result = ""
        for c in payload:
            if c.isalnum():
                result += c
            else:
                result += f"%u{ord(c):04x}"
        return result