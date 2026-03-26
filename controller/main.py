import logging
import time
from lib.injection.detector import InjectionDetector
from lib.injection.fingerprint import Fingerprinter
from lib.injection.exploit import ExploitEngine
from lib.takeover.os import OSShell
from lib.takeover.file import FileSystem
from core.exception import ShadowException

logger = logging.getLogger(__name__)

class ShadowController:
    def __init__(self, settings, session):
        self.settings = settings
        self.session = session
        self.vulnerabilities = []
        self.dbms = None
        
    def run(self):
        logger.info("SHADOWINJECT starting...")
        
        # Step 1: Detect injection points
        logger.info("Scanning for injection points...")
        detector = InjectionDetector(self.settings, self.session)
        self.vulnerabilities = detector.detect_all()
        
        if not self.vulnerabilities:
            logger.error("No injection points found. Exiting.")
            return
        
        # Step 2: Fingerprint DBMS
        logger.info("Fingerprinting database...")
        fingerprinter = Fingerprinter(self.settings, self.session)
        self.dbms = fingerprinter.fingerprint(self.vulnerabilities[0])
        logger.info(f"Identified DBMS: {self.dbms}")
        
        # Step 3: Execute requested action
        if self.settings.dbs:
            self.enumerate_databases()
        elif self.settings.tables:
            self.enumerate_tables(self.settings.tables)
        elif self.settings.columns:
            db, table = self.settings.columns.split('.')
            self.enumerate_columns(db, table)
        elif self.settings.dump:
            self.dump_table(self.settings.dump)
        elif self.settings.os_shell:
            self.os_shell()
        elif self.settings.file_read:
            self.file_read(self.settings.file_read)
        elif self.settings.file_write:
            local, remote = self.settings.file_write
            self.file_write(local, remote)
        else:
            # Default: show basic info
            self.show_info()
            
    def enumerate_databases(self):
        logger.info("Enumerating databases...")
        engine = ExploitEngine(self.settings, self.session, self.vulnerabilities[0])
        dbs = engine.enumerate_databases()
        for db in dbs:
            logger.info(f"[DB] {db}")
            
    def enumerate_tables(self, db_name):
        logger.info(f"Enumerating tables in {db_name}...")
        engine = ExploitEngine(self.settings, self.session, self.vulnerabilities[0])
        tables = engine.enumerate_tables(db_name)
        for table in tables:
            logger.info(f"[TABLE] {table}")
            
    def os_shell(self):
        logger.info("Attempting OS shell...")
        os_shell = OSShell(self.settings, self.session, self.vulnerabilities[0], self.dbms)
        os_shell.interact()
        
    def file_read(self, remote_path):
        fs = FileSystem(self.settings, self.session, self.vulnerabilities[0], self.dbms)
        content = fs.read_file(remote_path)
        if content:
            print(content)
        else:
            logger.error("Failed to read file")
            
    def file_write(self, local_path, remote_path):
        fs = FileSystem(self.settings, self.session, self.vulnerabilities[0], self.dbms)
        if fs.write_file(local_path, remote_path):
            logger.info(f"File written to {remote_path}")
        else:
            logger.error("Failed to write file")
            
    def show_info(self):
        logger.info("No specific action requested. Use --help for available actions.")
        logger.info(f"Found {len(self.vulnerabilities)} injection points")
        logger.info(f"DBMS: {self.dbms}")