import logging
from core.engine import InjectionEngine

logger = logging.getLogger(__name__)

class ActionHandler:
    def __init__(self, settings, session):
        self.settings = settings
        self.session = session
        self.engine = InjectionEngine(settings, session)
        
    def execute(self):
        """Execute requested action based on settings"""
        if not self.engine.scan():
            return
        
        if self.settings.dbs:
            self._enum_databases()
        elif self.settings.tables:
            self._enum_tables(self.settings.tables)
        elif self.settings.columns:
            self._enum_columns(self.settings.columns)
        elif self.settings.dump:
            self._dump_table(self.settings.dump)
        elif self.settings.os_shell:
            self._os_shell()
        elif self.settings.file_read:
            self._file_read(self.settings.file_read)
        elif self.settings.file_write:
            self._file_write(*self.settings.file_write)
        else:
            self._show_info()
            
    def _enum_databases(self):
        dbs = self.engine.enumerate_databases()
        print("\n[+] Databases found:")
        for db in dbs:
            print(f"  - {db}")
            
    def _enum_tables(self, db_name):
        tables = self.engine.enumerate_tables(db_name)
        print(f"\n[+] Tables in {db_name}:")
        for table in tables:
            print(f"  - {table}")
            
    def _enum_columns(self, db_table):
        parts = db_table.split('.')
        if len(parts) != 2:
            logger.error("Format must be database.table")
            return
        db, table = parts
        cols = self.engine.enumerate_columns(db, table)
        print(f"\n[+] Columns in {db}.{table}:")
        for col in cols:
            print(f"  - {col}")
            
    def _dump_table(self, db_table):
        parts = db_table.split('.')
        if len(parts) != 2:
            logger.error("Format must be database.table")
            return
        db, table = parts
        data = self.engine.dump_table(db, table)
        if data:
            print(f"\n[+] Data from {db}.{table}:")
            for row in data:
                print(" | ".join(str(cell) for cell in row))
        else:
            logger.info("No data found or extraction failed")
            
    def _os_shell(self):
        self.engine.os_shell()
        
    def _file_read(self, remote_path):
        content = self.engine.file_read(remote_path)
        if content:
            print(content)
        else:
            logger.error("Failed to read file")
            
    def _file_write(self, local, remote):
        if self.engine.file_write(local, remote):
            logger.info(f"File written to {remote}")
        else:
            logger.error("Failed to write file")
            
    def _show_info(self):
        print("\n[+] Injection points found:")
        for vuln in self.engine.vulnerabilities:
            print(f"  - Parameter: {vuln['param']} ({vuln['location']}) via {vuln['technique']}")
        print(f"[+] DBMS: {self.engine.dbms}")
        print("\n[!] Use --help to see available actions")