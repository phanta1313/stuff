#!/bin/bash

# Output Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}[*] Starting JavaScript collection process...${NC}"

# Check for input file
if [ ! -f "live_subdomains.txt" ]; then
    echo -e "${RED}[!] Error: live_subdomains.txt not found!${NC}"
    exit 1
fi

# 1. Collection via GAU
echo -e "${YELLOW}[1/5] Running GAU (Archived links)...${NC}"
cat live_subdomains.txt | ~/go/bin/gau --threads 10 | grep "\.js" >> js_urls_raw.txt
echo -e "${GREEN}[+] Done. GAU links added to js_urls_raw.txt${NC}"

# 2. Collection via Waybackurls
echo -e "${YELLOW}[2/5] Running Waybackurls...${NC}"
cat live_subdomains.txt | ~/go/bin/waybackurls >> js_urls_raw.txt
echo -e "${GREEN}[+] Done. Waybackurls links added to js_urls_raw.txt${NC}"

# 3. Active Crawling via Katana
echo -e "${YELLOW}[3/5] Running Katana (Active crawling)...${NC}"
katana -list live_subdomains.txt -jc -kf all -d 3 -o katana_js.txt
cat katana_js.txt | grep "\.js" >> js_urls_raw.txt
echo -e "${GREEN}[+] Done. Katana links added to js_urls_raw.txt${NC}"

# 4. Filtering and Cleaning
echo -e "${YELLOW}[4/5] Cleaning and removing duplicates...${NC}"
if [ -f "js_urls_raw.txt" ]; then
    sort -u js_urls_raw.txt | grep -vEi "\.(png|jpg|jpeg|gif|svg|woff|ttf|css)$" > js_urls_final.txt
    TOTAL=$(wc -l < js_urls_final.txt)
    echo -e "${GREEN}[+] Cleaning complete. Unique JS links found: ${TOTAL}${NC}"
else
    echo -e "${RED}[!] Error: js_urls_raw.txt is empty. Something went wrong.${NC}"
    exit 1
fi

# 5. Downloading via httpx
echo -e "${YELLOW}[5/5] Downloading content via httpx to 'js_files' directory...${NC}"
mkdir -p js_files
cat js_urls_final.txt | ~/go/bin/httpx -sr -srd js_files -mc 200

echo -e "${BLUE}--------------------------------------------------${NC}"
echo -e "${GREEN}[***] ALL STAGES COMPLETED!${NC}"
echo -e "${BLUE}[*] Final list saved to: js_urls_final.txt${NC}"
echo -e "${BLUE}[*] Files downloaded to directory: js_files${NC}"
echo -e "--------------------------------------------------"