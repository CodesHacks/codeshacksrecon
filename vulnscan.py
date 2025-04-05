import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from config import OWASP_TOP_10

def scan_vulnerabilities(url):
    """Scan for common web vulnerabilities"""
    vulnerabilities = []
    
    try:
        # Normalize URL
        if not url.startswith(('http://', 'https://')):
            url = f'http://{url}'

        # Check for SQL Injection potential
        if is_sqli_vulnerable(url):
            vulnerabilities.append({
                'type': 'SQL Injection',
                'severity': 'High',
                'description': 'Potential SQL injection vulnerability detected'
            })

        # Check for XSS potential
        if is_xss_vulnerable(url):
            vulnerabilities.append({
                'type': 'Cross-Site Scripting (XSS)',
                'severity': 'Medium',
                'description': 'Potential XSS vulnerability detected'
            })

        # Check for sensitive data exposure
        response = requests.get(url)
        if any(header in response.headers for header in ['X-Powered-By', 'Server']):
            vulnerabilities.append({
                'type': 'Sensitive Data Exposure',
                'severity': 'Low',
                'description': 'Server information exposed in headers'
            })

    except Exception as e:
        print(f"[!] Vulnerability scan failed: {e}")

    return vulnerabilities

def is_sqli_vulnerable(url):
    """Check for basic SQL injection vulnerability"""
    test_payloads = ["'", "\"", "1' OR '1'='1"]
    for payload in test_payloads:
        test_url = f"{url}?id={payload}"
        try:
            response = requests.get(test_url)
            if any(error in response.text.lower() for error in ['sql', 'syntax', 'database']):
                return True
        except:
            continue
    return False

def is_xss_vulnerable(url):
    """Check for basic XSS vulnerability"""
    test_payload = "<script>alert('XSS')</script>"
    test_url = f"{url}?q={test_payload}"
    try:
        response = requests.get(test_url)
        if test_payload in response.text:
            return True
    except:
        pass
    return False
