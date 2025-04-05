#!/usr/bin/env python3
import argparse
from modules import subdomains, techdetect, ports, vulnscan, report
from config import DEFAULT_TARGET, REPORT_DIR
import os

def main():
    parser = argparse.ArgumentParser(description="CodeShacks - Comprehensive Web Recon Tool")
    parser.add_argument("-t", "--target", help="Target domain or IP", default=DEFAULT_TARGET)
    parser.add_argument("-o", "--output", help="Output directory", default=REPORT_DIR)
    parser.add_argument("--passive", help="Passive reconnaissance only", action="store_true")
    parser.add_argument("--full", help="Full active scan", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    print(f"[*] Starting CodeShacks scan for {args.target}")
    
    # Run modules
    results = {
        'subdomains': subdomains.find_subdomains(args.target),
        'technologies': techdetect.detect_technologies(args.target),
        'ports': ports.scan_ports(args.target),
        'vulnerabilities': vulnscan.scan_vulnerabilities(args.target)
    }

    # Generate report
    report.generate_html_report(results, args.output)
    print(f"[+] Scan completed. Report saved to {args.output}")

if __name__ == "__main__":
    main()
