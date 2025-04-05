 #!/usr/bin/env python3
import argparse
from modules import subdomains, techdetect, ports, vulnscan, report
from config import DEFAULT_TARGET, REPORT_DIR
import os

def main():
    parser = argparse.ArgumentParser(description="CodeShacks - Comprehensive Web Recon Tool")
    parser.add_argument("-t", "--target", help="Target domain or IP", default=DEFAULT_TARGET)
    parser.add_argument("-o", "--output", help="Output directory", default=REPORT_DIR)
    
    # Scan type options
    scan_group = parser.add_mutually_exclusive_group()
    scan_group.add_argument("--fast", help="Fast scan (subdomains + common ports)", action="store_true")
    scan_group.add_argument("--deep", help="Deep scan (all checks + full port range)", action="store_true")
    scan_group.add_argument("--vuln", help="Vulnerability scan only", action="store_true")
    
    # Module options
    parser.add_argument("--no-subdomains", help="Skip subdomain discovery", action="store_true")
    parser.add_argument("--no-tech", help="Skip technology detection", action="store_true")
    parser.add_argument("-p", "--ports", help="Custom port range (e.g. 80,443,8000-9000)")
    
    # Exploitation options
    exploit_group = parser.add_argument_group('Exploitation Options')
    exploit_group.add_argument("--exploit", help="Attempt to exploit found vulnerabilities", action="store_true")
    exploit_group.add_argument("--interactive", help="Interactive exploitation mode", action="store_true")
    exploit_group.add_argument("--payload", help="Custom payload file for exploitation")
    
    # Output options
    parser.add_argument("--json", help="Output JSON report instead of HTML", action="store_true")
    parser.add_argument("--quiet", help="Suppress console output", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if not args.quiet:
        print(f"[*] Starting CodeShacks scan for {args.target}")

    results = {}
    
    # Determine port range
    scan_ports = None
    if args.ports:
        scan_ports = []
        for part in args.ports.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                scan_ports.extend(range(start, end+1))
            else:
                scan_ports.append(int(part))
    
    # Run modules based on scan type
    if not args.no_subdomains and (not args.vuln or args.deep):
        results['subdomains'] = subdomains.find_subdomains(args.target)
    
    if not args.no_tech and (not args.vuln or args.deep):
        results['technologies'] = techdetect.detect_technologies(args.target)
    
    if not args.vuln:
        results['ports'] = ports.scan_ports(args.target, scan_ports)
    
    if args.vuln or args.deep:
        results['vulnerabilities'] = vulnscan.scan_vulnerabilities(args.target)

    # Generate report
    if args.json:
        report.generate_json_report(results, args.output)
        if not args.quiet:
            print(f"[+] JSON report saved to {args.output}/report.json")
    else:
        report.generate_html_report(results, args.output)
        if not args.quiet:
            print(f"[+] HTML report saved to {args.output}/report.html")

if __name__ == "__main__":
    main()
