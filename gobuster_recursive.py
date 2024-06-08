import os
import subprocess
import sys

def run_gobuster(url):
    command = f"gobuster dir -u {url} -w /usr/share/wordlists/SecLists/Discovery/Web-Content/common.txt"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return result.stdout

def extract_directories(scan_output):
    directories = []
    for line in scan_output.splitlines():
        if '404' not in line:
            parts = line.split()
            directories.append(parts[0])
    return directories

def main(base_url, output_file):
    scan_queue = [base_url]
    scanned = set()

    with open(output_file, 'a') as outfile:
        while scan_queue:
            url = scan_queue.pop(0)
            if url in scanned:
                continue

            print(f"Scanning {url} - results will be appended to {output_file}")
            scan_output = run_gobuster(url)
            outfile.write(f"\nResults for {url}:\n")
            outfile.write(scan_output)
            outfile.write("\n")

            scanned.add(url)
            new_directories = extract_directories(scan_output)
            for directory in new_directories:
                new_url = f"{url.rstrip('/')}/{directory.lstrip('/')}"
                if new_url not in scanned:
                    scan_queue.append(new_url)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python recursive_gobuster.py <IP_ADDRESS>")
        sys.exit(1)

    ip_address = sys.argv[1]
    base_url = f"http://{ip_address}"
    output_file = "80/gobuster_recursive_results.txt"
    os.makedirs("80", exist_ok=True)
    main(base_url, output_file)

