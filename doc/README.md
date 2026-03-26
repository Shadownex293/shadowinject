# SHADOWINJECT

Advanced SQL injection and database takeover tool.  
Built for penetration testing and security research.

## Features

- Automatic detection of injection points (GET, POST, Cookie, Headers)
- Multiple injection techniques: boolean, time, error, union
- Database fingerprinting
- Data extraction (databases, tables, columns, rows)
- File system read/write (where supported)
- OS shell via UDF or stored procedures
- Tamper scripts for WAF bypass
- Extensible plugin system

## Installation

```bash
git clone https://github.com/yourname/shadowinject.git
cd shadowinject
pip install -r requirements.txt