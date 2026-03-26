import time
import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urlparse, parse_qs, urlencode

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self, settings):
        self.settings = settings
        self.session = self._create_session()
        
    def _create_session(self):
        session = requests.Session()
        retry = Retry(
            total=self.settings.retries,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        if self.settings.proxy:
            session.proxies = {"http": self.settings.proxy, "https": self.settings.proxy}
            
        if self.settings.cookie:
            session.cookies.update(self.settings.cookie_params)
            
        if self.settings.headers:
            session.headers.update(self.settings.headers)
            
        session.headers['User-Agent'] = self.settings.user_agent or \
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            
        return session

class Request:
    def __init__(self, session, settings):
        self.session = session
        self.settings = settings
        
    def send(self, param, value, location="GET"):
        """Send request with modified parameter"""
        time.sleep(self.settings.delay)
        
        if location == "GET":
            url = self._build_get_url(param, value)
            try:
                resp = self.session.get(url, timeout=self.settings.timeout)
                return resp
            except Exception as e:
                logger.debug(f"Request failed: {e}")
                return None
                
        elif location == "POST":
            data = self.settings.post_params.copy()
            data[param] = value
            try:
                resp = self.session.post(self.settings.url, data=data, timeout=self.settings.timeout)
                return resp
            except Exception:
                return None
                
        elif location == "COOKIE":
            cookies = self.settings.cookie_params.copy()
            cookies[param] = value
            self.session.cookies.update(cookies)
            try:
                resp = self.session.get(self.settings.url, timeout=self.settings.timeout)
                return resp
            except Exception:
                return None
        return None
        
    def send_raw(self, url, method='GET', data=None, headers=None):
        """Send raw HTTP request without parameter manipulation"""
        time.sleep(self.settings.delay)
        try:
            if method.upper() == 'GET':
                resp = self.session.get(url, timeout=self.settings.timeout, headers=headers)
            else:
                resp = self.session.post(url, data=data, timeout=self.settings.timeout, headers=headers)
            return resp
        except Exception as e:
            logger.debug(f"Raw request failed: {e}")
            return None
        
    def _build_get_url(self, param, value):
        parsed = urlparse(self.settings.url)
        qs = parse_qs(parsed.query, keep_blank_values=True)
        qs[param] = [value]
        new_query = urlencode(qs, doseq=True)
        return parsed._replace(query=new_query).geturl()