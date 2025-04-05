import socket
from concurrent.futures import ThreadPoolExecutor
from config import COMMON_PORTS
import time

def scan_port(target, port):
    """Scan a single port on target"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                try:
                    service = socket.getservbyport(port)
                except:
                    service = "unknown"
                return (port, service, "open")
    except:
        pass
    return None

def scan_ports(target, ports=None):
    """Scan multiple ports on target using threading"""
    open_ports = []
    ports = ports or COMMON_PORTS
    
    print(f"[*] Scanning {len(ports)} ports on {target}")
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(scan_port, target, port) for port in ports]
        for future in futures:
            result = future.result()
            if result:
                port, service, status = result
                print(f"[+] Port {port} ({service}) is {status}")
                open_ports.append({
                    'port': port,
                    'service': service,
                    'status': status
                })
    
    return open_ports
