for file in */*.txt; do 
    echo "[*] Checking $file..."
    python3 ~/awesome_things/scripts/secret_finder.py -i "$file" -o cli >> all_secrets.txt 2>/dev/null
done
