from .base import TamperBase

class Space2Plus(TamperBase):
    def __init__(self):
        self.name = "space2plus"
        
    def tamper(self, payload):
        # Replace spaces with '+'
        return payload.replace(' ', '+')