from .base import TamperBase

class ApostropheMask(TamperBase):
    def __init__(self):
        self.name = "apostrophemask"
        
    def tamper(self, payload):
        # Replace apostrophe with UTF-8 equivalent
        return payload.replace("'", "’")