import re
import time
from collections import deque

class WAFDetector:
    COMMON_WAF_SIGNATURES = {
        'Cloudflare': r'cloudflare',
        'ModSecurity': r'Mod_Security|NOYB',
        'AWS WAF': r'awselb',
        'F5 BIG-IP': r'F5|BigIP',
        'Sucuri': r'Sucuri|Cloudproxy',
        'Imperva': r'Incapsula',
        'Akamai': r'AkamaiGHost',
        'Barracuda': r'barracuda',
        'Fortinet': r'FortiWeb',
    }

    @staticmethod
    def detect_waf(response_headers, response_body):
        headers_str = str(response_headers).lower()
        body_str = response_body.lower() if response_body else ''
        for waf, pattern in WAFDetector.COMMON_WAF_SIGNATURES.items():
            if re.search(pattern, headers_str) or re.search(pattern, body_str):
                return waf
        return None

    @staticmethod
    def is_blocked(response):
        """Check if response indicates WAF blocking"""
        if response.status_code in [403, 406, 429, 503]:
            return True
        body = response.text.lower()
        block_keywords = ['blocked', 'forbidden', 'access denied', 'security', 'attack detected']
        for kw in block_keywords:
            if kw in body:
                return True
        return False

class RateLimiter:
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window = window_seconds
        self.timestamps = deque()

    def wait_if_needed(self):
        """Sleep if rate limit would be exceeded"""
        now = time.time()
        # Remove old timestamps
        while self.timestamps and now - self.timestamps[0] > self.window:
            self.timestamps.popleft()
        if len(self.timestamps) >= self.max_requests:
            sleep_time = self.window - (now - self.timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)
        self.timestamps.append(time.time())