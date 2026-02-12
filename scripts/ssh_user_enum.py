import paramiko
import os
import argparse
import socket
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser(prog="SSH User Enumerator Multi-threaded")
parser.add_argument('ip')
parser.add_argument('port', type=int)
parser.add_argument('wordlist_path')
parser.add_argument('id_rsa_path')
parser.add_argument('--threads', type=int, default=5, help="Количество потоков (default: 5)")
args = parser.parse_args()

key_path = os.path.expanduser(args.id_rsa_path)
private_key = paramiko.RSAKey.from_private_key_file(key_path)

def check_user(username):
    username = username.strip()
    if not username:
        return
    
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(
            hostname=args.ip,
            port=args.port,
            username=username,
            pkey=private_key,
            timeout=7,
            allow_agent=False,
            look_for_keys=False
        )
        print(f"\n[+] SUCCESS: User '{username}' found and logged in!")
        client.close()
    except paramiko.AuthenticationException:
        print(f"[-] {username}: Authentication failed (User might not exist or key rejected)")
    except socket.error:
        print(f"[!] {username}: Connection timeout/error")
    except Exception as e:
        print(f"[!] {username}: Error: {e}")
        try: client.close()
        except: pass

def main():
    try:
        with open(args.wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            users = f.readlines()
    except FileNotFoundError:
        print(f"File {args.wordlist_path} not found.")
        return

    print(f"[*] Starting enumeration on {args.ip}:{args.port} using {args.threads} threads...")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(check_user, users)

if __name__ == "__main__":
    main()
