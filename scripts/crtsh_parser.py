import requests
from bs4 import BeautifulSoup
import argparse
import sys

parser = argparse.ArgumentParser(description='crt.sh parser')
parser.add_argument('target', help='Домен для поиска (например, pinterest.com)')
args = parser.parse_args()

url = f"https://crt.sh/?q={args.target}"
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}

try:
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
except Exception as e:
    print(f"[!] Crt.sh server error. {e}")
    sys.exit(1)

soup = BeautifulSoup(response.text, 'html.parser')
subdomains = set()

for tr in soup.find_all('tr'):
    tds = tr.find_all('td')
    if len(tds) > 4:
       
        content = tds[4].get_text(separator="\n").split('\n')
        for domain in content:
            clean_domain = domain.strip().lower().replace("*.", "")
            if clean_domain.endswith(args.target):
                subdomains.append(clean_domain) if isinstance(subdomains, list) else subdomains.add(clean_domain)

for sub in sorted(subdomains):
    print(sub)

