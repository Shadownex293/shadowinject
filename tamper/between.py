class Between(TamperBase):
    def __init__(self):
        self.name = "between"
        
    def tamper(self, payload):
        # Replace 'AND' with 'BETWEEN'
        return payload.replace('AND', 'BETWEEN')