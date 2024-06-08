import subprocess
import argparse
import re
import os

def run_wfuzz(url, wordlist, output_file):
    command = f"wfuzz -c -z file,{wordlist} --follow --sc 200,301 -u {url}/FUZZ"
    print(f"Running command: {command}")
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    clean_output = strip_ansi_codes(result.stdout)
    with open(output_file, "a") as outfile:
        outfile.write(clean_output)
    return clean_output

def strip_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text)

def parse_wfuzz_output(output):
    results = []
    for line in output.splitlines():
        match = re.search(r'(\d{6}):  C=(\d{3})\s+\d+ L\s+\d+ W\s+\d+ Ch\s+"([^"]+)"', line)
        if match:
            status_code = match.group(2)
            path = match.group(3)
            results.append((status_code, path))
    return results

def scan_url_recursively(base_url, wordlist, output_file):
    to_scan = [base_url]
    scanned = set()
    
    while to_scan:
        current_url = to_scan.pop(0)
        if current_url in scanned:
            continue
        
        print(f"Scanning URL: {current_url}")
        output = run_wfuzz(current_url, wordlist, output_file)
        results = parse_wfuzz_output(output)
        scanned.add(current_url)
        
        for status_code, path in results:
            full_url = f"{current_url.rstrip('/')}/{path.lstrip('/')}"
            if status_code == '301':
                print(f"301 Moved Permanently found at: {full_url}, adding to scan list")
                to_scan.append(full_url)
            elif status_code == '200':
                print(f"200 OK found at: {full_url}")
                append_to_file(full_url, "200_urls.txt")
                to_scan.append(full_url)  # Add 200 URL back to the scan list for further scanning

def append_to_file(url, file_path):
    with open(file_path, "a") as file:
        file.write(f"200 OK found at: {url}\n")

def main():
    parser = argparse.ArgumentParser(description="Recursively scan URLs for 301 redirects until a 200 status code is found.")
    parser.add_argument("url", help="The URL to scan")
    parser.add_argument("wordlist", help="The wordlist to use for fuzzing")
    args = parser.parse_args()
    
    # Remove the file if it exists to start fresh
    if os.path.exists("200_urls.txt"):
        os.remove("200_urls.txt")
    
    # Run wfuzz on the provided URL recursively
    scan_url_recursively(args.url, args.wordlist, "wfuzz_200_results.txt")

if __name__ == "__main__":
    main()
