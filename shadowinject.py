#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SHADOWINJECT v2.0 - Automatic SQL Injection and Database Takeover Tool
Author: SHADOWAI
"""

import sys
import os
import argparse
import logging

# Add current directory to path for internal imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.settings import Settings
from controller.main import ShadowController
from lib.request.client import SessionManager

def main():
    parser = argparse.ArgumentParser(description="SHADOWINJECT - Advanced SQLi Framework")
    
    # Target options
    target = parser.add_argument_group("Target")
    target.add_argument("-u", "--url", help="Target URL")
    target.add_argument("--data", help="POST data")
    target.add_argument("--cookie", help="HTTP Cookie")
    target.add_argument("--headers", help="Extra headers (JSON)")
    target.add_argument("--proxy", help="Proxy URL (e.g., socks5://127.0.0.1:9050)")
    
    # Detection options
    detect = parser.add_argument_group("Detection")
    detect.add_argument("--level", type=int, default=1, choices=range(1,6), help="Level of tests (1-5)")
    detect.add_argument("--risk", type=int, default=1, choices=range(1,4), help="Risk of tests (1-3)")
    
    # Exploitation options
    exploit = parser.add_argument_group("Exploitation")
    exploit.add_argument("--dbs", action="store_true", help="Enumerate databases")
    exploit.add_argument("--tables", help="Enumerate tables of a database")
    exploit.add_argument("--columns", help="Enumerate columns of a table (format: DB.TABLE)")
    exploit.add_argument("--dump", help="Dump table data (format: DB.TABLE[.COLUMN])")
    exploit.add_argument("--os-shell", action="store_true", help="Prompt for OS shell")
    exploit.add_argument("--file-read", help="Read a file from server")
    exploit.add_argument("--file-write", nargs=2, metavar=("LOCAL", "REMOTE"), help="Write local file to remote")
    
    # Optimization
    opt = parser.add_argument_group("Optimization")
    opt.add_argument("--threads", type=int, default=1, help="Number of threads")
    opt.add_argument("--delay", type=float, default=0, help="Delay between requests (seconds)")
    opt.add_argument("--timeout", type=int, default=30, help="Request timeout")
    opt.add_argument("--retries", type=int, default=3, help="Retries on failure")
    
    # Misc
    misc = parser.add_argument_group("Misc")
    misc.add_argument("-v", "--verbose", action="count", default=0, help="Verbosity level")
    misc.add_argument("--batch", action="store_true", help="Never ask for user input")
    misc.add_argument("--flush-session", action="store_true", help="Flush session files")
    
    args = parser.parse_args()
    
    if not args.url:
        parser.print_help()
        sys.exit(1)
    
    # Setup logging
    logging.basicConfig(level=logging.DEBUG if args.verbose > 1 else logging.INFO)
    
    # Initialize settings
    settings = Settings(args)
    
    # Initialize session manager
    session = SessionManager(settings)
    
    # Run controller
    controller = ShadowController(settings, session)
    controller.run()

if __name__ == "__main__":
    main()