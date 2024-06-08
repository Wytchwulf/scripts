import subprocess
import argparse
import re
import os

def run_gobuster(url):
    command = f"gobuster dir -u {url} -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt -o gobuster_output.txt -q"
    print(f"Running command: {command}")
    subprocess.run(command, shell=True, check=True)

def parse_gobuster_output():
    results = []
    with open("gobuster_output.txt", "r") as file:
        for line in file:
            match = re.search(r'(.+?) \((Status: )(\d+)\)', line)
            if match:
                path = match.group(1)
                status_code = match.group(3)
                results.append((status_code, path))
    return results

def append_to_file(url):
    with open("200_urls.txt", "a") as file:
        file.write(f"200 OK found at: {url}\n")

def scan_url_until_200(base_url):
    to_scan = [base_url]
    scanned = set()
    
    while to_scan:
        current_url = to_scan.pop(0)
        if current_url in scanned:
            continue
        
        print(f"Scanning URL: {current_url}")
        run_gobuster(current_url)
        results = parse_gobuster_output()
        scanned.add(current_url)
        
        for status_code, path in results:
            full_url = f"{current_url.rstrip('/')}/{path.lstrip('/')}"
            if status_code == '301':
                print(f"301 Moved Permanently found at: {full_url}, adding to scan list")
                to_scan.append(full_url)
            elif status_code == '200':
                print(f"200 OK found at: {full_url}")
                append_to_file(full_url)

def main():
    parser = argparse.ArgumentParser(description="Recursively scan URLs for 301 redirects until a 200 status code is found.")
    parser.add_argument("url", help="The URL to scan")
    args = parser.parse_args()
    
    # Remove the file if it exists to start fresh
    if os.path.exists("200_urls.txt"):
        os.remove("200_urls.txt")
    
    scan_url_until_200(args.url)

if __name__ == "__main__":
    main()



