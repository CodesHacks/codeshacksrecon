from datetime import datetime
from config import REPORT_DIR
import os

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeShacks Report</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto px-4 py-8">
        <header class="bg-white shadow rounded-lg p-6 mb-8">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-3xl font-bold text-gray-800">CodeShacks Report</h1>
                    <p class="text-gray-600">Generated on {generation_date}</p>
                </div>
                <div class="bg-blue-100 p-3 rounded-full">
                    <i class="fas fa-shield-alt text-blue-600 text-2xl"></i>
                </div>
            </div>
        </header>

        <div class="grid gap-8">
            <!-- Subdomains Section -->
            <section class="bg-white shadow rounded-lg p-6">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">
                    <i class="fas fa-sitemap mr-2 text-blue-500"></i>
                    Subdomains Found ({subdomain_count})
                </h2>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Subdomain</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            {subdomain_rows}
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- Technologies Section -->
            <section class="bg-white shadow rounded-lg p-6">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">
                    <i class="fas fa-code mr-2 text-blue-500"></i>
                    Technologies Detected
                </h2>
                <div class="flex flex-wrap gap-4">
                    {technology_cards}
                </div>
            </section>

            <!-- Open Ports Section -->
            <section class="bg-white shadow rounded-lg p-6">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">
                    <i class="fas fa-plug mr-2 text-blue-500"></i>
                    Open Ports ({port_count})
                </h2>
                <div class="overflow-x-auto">
                    <table class="min-w-full divide-y divide-gray-200">
                        <thead class="bg-gray-50">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Port</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Service</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                            </tr>
                        </thead>
                        <tbody class="bg-white divide-y divide-gray-200">
                            {port_rows}
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- Vulnerabilities Section -->
            <section class="bg-white shadow rounded-lg p-6">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">
                    <i class="fas fa-bug mr-2 text-blue-500"></i>
                    Vulnerabilities Found ({vulnerability_count})
                </h2>
                <div class="space-y-4">
                    {vulnerability_cards}
                </div>
            </section>
        </div>
    </div>
</body>
</html>
"""

def generate_html_report(data, output_dir):
    """Generate HTML report from scan results"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    report_path = os.path.join(output_dir, "report.html")
    generation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Prepare subdomains data
    subdomain_rows = ""
    for sub in data.get('subdomains', []):
        subdomain_rows += f"""
            <tr>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{sub}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Active</span>
                </td>
            </tr>
        """

    # Prepare technologies data
    technology_cards = ""
    tech_data = data.get('technologies', {})
    for tech_type, value in tech_data.items():
        if isinstance(value, list):
            for item in value:
                technology_cards += create_tech_card(item, tech_type)
        elif value:
            technology_cards += create_tech_card(value, tech_type)

    # Prepare ports data
    port_rows = ""
    for port in data.get('ports', []):
        port_rows += f"""
            <tr>
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{port['port']}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{port['service']}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">Open</span>
                </td>
            </tr>
        """

    # Prepare vulnerabilities data
    vulnerability_cards = ""
    for vuln in data.get('vulnerabilities', []):
        severity_color = {
            'High': 'red',
            'Medium': 'yellow',
            'Low': 'blue'
        }.get(vuln['severity'], 'gray')
        
        vulnerability_cards += f"""
            <div class="p-4 border-l-4 border-{severity_color}-500 bg-white rounded-lg shadow-sm">
                <div class="flex items-start justify-between">
                    <div>
                        <h3 class="font-medium text-gray-900">{vuln['type']}</h3>
                        <p class="text-sm text-gray-500">{vuln['description']}</p>
                    </div>
                    <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-{severity_color}-100 text-{severity_color}-800">
                        {vuln['severity']}
                    </span>
                </div>
            </div>
        """

    # Format the HTML template with data
    report_html = HTML_TEMPLATE.format(
        generation_date=generation_date,
        subdomain_count=len(data.get('subdomains', [])),
        subdomain_rows=subdomain_rows,
        technology_cards=technology_cards,
        port_count=len(data.get('ports', [])),
        port_rows=port_rows,
        vulnerability_count=len(data.get('vulnerabilities', [])),
        vulnerability_cards=vulnerability_cards
    )

    # Write the report file
    with open(report_path, 'w') as f:
        f.write(report_html)

    return report_path

def create_tech_card(tech_name, tech_type):
    """Create a technology card for the report"""
    icons = {
        'server': 'server',
        'framework': 'layer-group',
        'javascript': 'js',
        'analytics': 'chart-line',
        'cms': 'box'
    }
    return f"""
        <div class="flex items-center p-4 bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="p-3 mr-4 text-blue-500 bg-blue-100 rounded-full">
                <i class="fas fa-{icons.get(tech_type, 'code')}"></i>
            </div>
            <div>
                <p class="text-sm font-medium text-gray-900">{tech_name}</p>
                <p class="text-xs text-gray-500 capitalize">{tech_type}</p>
            </div>
        </div>
    """
