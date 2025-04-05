import requests
import dns.resolver
from config import SUBDOMAIN_LIST_PATH
import os

def find_subdomains(domain):
    """Discover subdomains using DNS resolution and HTTP checks"""
    subdomains = set()
    
    # Check if wordlist exists
    if not os.path.exists(SUBDOMAIN_LIST_PATH):
        print(f"[!] Subdomain wordlist not found at {SUBDOMAIN_LIST_PATH}")
        return list(subdomains)

    # Read subdomains from wordlist
    with open(SUBDOMAIN_LIST_PATH) as f:
        wordlist = [line.strip() for line in f]

    print(f"[*] Checking {len(wordlist)} subdomains for {domain}")
    
    for sub in wordlist:
        full_domain = f"{sub}.{domain}"
        try:
            # DNS resolution check
            answers = dns.resolver.resolve(full_domain, 'A')
            if answers:
                subdomains.add(full_domain)
                print(f"[+] Found subdomain: {full_domain}")
        except:
            continue

    return list(subdomains)

def passive_discovery(domain):
    """Passive subdomain discovery using public APIs"""
    try:
        response = requests.get(f"https://crt.sh/?q=%25.{domain}&output=json")
        if response.status_code == 200:
            data = response.json()
            return [item['name_value'] for item in data]
    except Exception as e:
        print(f"[!] Passive discovery failed: {e}")
    return []
