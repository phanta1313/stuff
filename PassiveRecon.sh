#!/bin/bash

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' 

if [ -z "$1" ]; then
    echo -e "${YELLOW}Usage: $0 target.com${NC}"
    exit 1
fi

target=$1
echo -e "${CYAN}[*] Starting recon for: ${YELLOW}$target${NC}"

echo -e "${GREEN}[+] Extracting subdomains...${NC}"

subfinder -d "$target" -silent | ~/go/bin/httpx -silent > domains_temp.txt

sort -u domains_temp.txt -o domains.txt
rm domains_temp.txt

echo -e "${CYAN}[i] Found $(wc -l < domains.txt) alive domains. Saved to domains.txt${NC}"

echo -e "${GREEN}[+] Crawling URLs...${NC}"

katana -list domains.txt -silent > urls_temp.txt

sort -u urls_temp.txt -o urls.txt
rm urls_temp.txt

echo -e "${CYAN}[i] Found $(wc -l < urls.txt) unique URLs. Saved to urls.txt${NC}"
echo -e "${YELLOW}--- Recon Complete ---${NC}"
