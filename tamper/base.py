import re
import random

class TamperBase:
    """Base class for tamper scripts"""
    def __init__(self):
        self.name = "base"
        
    def tamper(self, payload):
        return payload

class RandomCase(TamperBase):
    def __init__(self):
        self.name = "randomcase"
        
    def tamper(self, payload):
        result = ""
        for c in payload:
            if c.isalpha() and random.choice([True, False]):
                result += c.upper()
            else:
                result += c
        return result

class Space2Comment(TamperBase):
    def __init__(self):
        self.name = "space2comment"
        
    def tamper(self, payload):
        # Replace spaces with /**/
        return re.sub(r'\s+', '/**/', payload)

class CharEncode(TamperBase):
    def __init__(self):
        self.name = "charencode"
        
    def tamper(self, payload):
        # URL encode all characters
        return ''.join(f'%{ord(c):02x}' for c in payload)