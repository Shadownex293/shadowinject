import json
from urllib.parse import parse_qs, urlparse

class Settings:
    def __init__(self, args):
        self.url = args.url
        self.data = args.data
        self.cookie = args.cookie
        self.headers = json.loads(args.headers) if args.headers else {}
        self.proxy = args.proxy
        self.level = args.level
        self.risk = args.risk
        self.threads = args.threads
        self.delay = args.delay
        self.timeout = args.timeout
        self.retries = args.retries
        self.verbose = args.verbose
        self.batch = args.batch
        self.flush_session = args.flush_session
        
        # Parse target for parameters
        self.get_params = {}
        self.post_params = {}
        self.cookie_params = {}
        
        parsed = urlparse(self.url)
        if parsed.query:
            self.get_params = parse_qs(parsed.query, keep_blank_values=True)
            # Convert list values to single string
            for k, v in self.get_params.items():
                self.get_params[k] = v[0] if v else ''
        
        if self.data:
            self.post_params = parse_qs(self.data, keep_blank_values=True)
            for k, v in self.post_params.items():
                self.post_params[k] = v[0] if v else ''
        
        if self.cookie:
            self.cookie_params = parse_qs(self.cookie, keep_blank_values=True)
            for k, v in self.cookie_params.items():
                self.cookie_params[k] = v[0] if v else ''
                
        # Actions
        self.dbs = args.dbs
        self.tables = args.tables
        self.columns = args.columns
        self.dump = args.dump
        self.os_shell = args.os_shell
        self.file_read = args.file_read
        self.file_write = args.file_write
        
        # User-Agent default
        self.user_agent = self.headers.get('User-Agent')