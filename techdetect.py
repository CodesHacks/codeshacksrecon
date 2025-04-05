import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def detect_technologies(url):
    """Detect web technologies used by a target"""
    technologies = {
        'server': None,
        'framework': None,
        'javascript': [],
        'analytics': None,
        'cms': None
    }

    try:
        # Normalize URL to include scheme
        if not url.startswith(('http://', 'https://')):
            url = f'http://{url}'

        response = requests.get(url, timeout=10)
        headers = response.headers

        # Check server headers
        technologies['server'] = headers.get('Server') or headers.get('X-Powered-By')

        # Parse HTML for framework clues
        soup = BeautifulSoup(response.text, 'html.parser')
        meta = soup.find_all('meta')

        # Detect common frameworks/CMS
        for tag in meta:
            if 'generator' in tag.get('name', '').lower():
                technologies['framework'] = tag.get('content')
            elif 'wordpress' in str(tag).lower():
                technologies['cms'] = 'WordPress'
            elif 'django' in str(tag).lower():
                technologies['framework'] = 'Django'

        # Detect JavaScript libraries
        scripts = soup.find_all('script', {'src': True})
        for script in scripts:
            src = script['src']
            if 'jquery' in src.lower():
                technologies['javascript'].append('jQuery')
            elif 'react' in src.lower():
                technologies['javascript'].append('React')
            elif 'vue' in src.lower():
                technologies['javascript'].append('Vue.js')

        # Detect analytics
        if 'google-analytics' in response.text.lower():
            technologies['analytics'] = 'Google Analytics'

    except Exception as e:
        print(f"[!] Technology detection failed: {e}")

    return {k: v for k, v in technologies.items() if v}
