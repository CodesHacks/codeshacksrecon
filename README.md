# CodeShacks - Comprehensive Web Recon Tool

![CodeShacks Logo](![logo](https://github.com/user-attachments/assets/1a9e3054-ffae-40b8-a781-88f07658a964)


A Python-based reconnaissance tool for web security assessments by Raj Shrivastav.

## Features
- Passive/Active reconnaissance
- Subdomain discovery
- Technology detection
- Port scanning
- OWASP Top 10 vulnerability scanning
- Automated HTML report generation

## Installation
1. Clone the repository:
```bash
git clone https://github.com/rajshrivastav/codeshacks.git
cd codeshacks
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
```bash
python codeshacks.py -t example.com -o ./reports/
```

### Options
- `-t/--target`: Target domain or IP (default: example.com)
- `-o/--output`: Output directory for reports (default: ./reports/)
- `--passive`: Passive reconnaissance only
- `--full`: Full active scan (includes vulnerability checks)

## Modules
1. **Subdomain Discovery**:
   - Uses DNS resolution and HTTP checks
   - Supports passive discovery via crt.sh

2. **Technology Detection**:
   - Identifies web servers, frameworks, CMS
   - Detects JavaScript libraries and analytics tools

3. **Port Scanning**:
   - Scans common ports (21, 22, 80, 443, etc.)
   - Multi-threaded for faster scanning

4. **Vulnerability Scanning**:
   - Checks for OWASP Top 10 vulnerabilities
   - Includes SQLi, XSS, and sensitive data exposure checks

5. **Report Generation**:
   - Beautiful HTML reports with Tailwind CSS
   - Includes all findings in organized sections

## Example Report
![Sample Report](https://via.placeholder.com/600x400?text=Sample+Report)

## License
MIT License

## Author
Raj Shrivastav - [@rajshrivastav](https://github.com/rajshrivastav)
