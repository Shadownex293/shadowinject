import logging
from lib.request.client import Request
from lib.injection.detector import InjectionDetector
from lib.injection.fingerprint import Fingerprinter
from lib.injection.exploit import ExploitEngine
from lib.takeover.os import OSShell
from lib.takeover.file import FileSystem

logger = logging.getLogger(__name__)

class InjectionEngine:
    """Main facade for injection operations"""
    
    def __init__(self, settings, session):
        self.settings = settings
        self.session = session
        self.vulnerabilities = []
        self.dbms = None
        self.detector = InjectionDetector(settings, session)
        self.fingerprinter = Fingerprinter(settings, session)
        
    def scan(self):
        """Detect injection points and fingerprint DBMS"""
        logger.info("Scanning for injection points...")
        self.vulnerabilities = self.detector.detect_all()
        if not self.vulnerabilities:
            logger.error("No injection points found")
            return False
        logger.info(f"Found {len(self.vulnerabilities)} injection points")
        self.dbms = self.fingerprinter.fingerprint(self.vulnerabilities[0])
        logger.info(f"Identified DBMS: {self.dbms}")
        return True
    
    def get_engine_for_vuln(self, vuln=None):
        """Get exploit engine for given vulnerability (or first)"""
        if vuln is None:
            if not self.vulnerabilities:
                return None
            vuln = self.vulnerabilities[0]
        engine = ExploitEngine(self.settings, self.session, vuln)
        engine.dbms = self.dbms
        return engine
    
    def enumerate_databases(self):
        engine = self.get_engine_for_vuln()
        if engine:
            return engine.enumerate_databases()
        return []
    
    def enumerate_tables(self, db_name):
        engine = self.get_engine_for_vuln()
        if engine:
            return engine.enumerate_tables(db_name)
        return []
    
    def enumerate_columns(self, db_name, table_name):
        engine = self.get_engine_for_vuln()
        if engine:
            return engine.enumerate_columns(db_name, table_name)
        return []
    
    def dump_table(self, db_name, table_name):
        engine = self.get_engine_for_vuln()
        if engine:
            return engine.dump_table(db_name, table_name)
        return []
    
    def os_shell(self):
        if not self.vulnerabilities:
            return False
        os_shell = OSShell(self.settings, self.session, self.vulnerabilities[0], self.dbms)
        os_shell.interact()
        return True
    
    def file_read(self, remote_path):
        fs = FileSystem(self.settings, self.session, self.vulnerabilities[0], self.dbms)
        return fs.read_file(remote_path)
    
    def file_write(self, local_path, remote_path):
        fs = FileSystem(self.settings, self.session, self.vulnerabilities[0], self.dbms)
        return fs.write_file(local_path, remote_path)