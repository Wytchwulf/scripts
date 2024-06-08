import os
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python run_nmap_scan.py <IP_ADDRESS> <PORTSCAN_FILE_PATH>")
        sys.exit(1)

    IP = sys.argv[1]
    portscan_file_path = sys.argv[2]

    # Read the port scan result file
    with open(portscan_file_path, 'r') as file:
        lines = file.readlines()

    # Extract port numbers from the file
    ports = []
    for line in lines:
        if '/tcp' in line:
            port = line.split('/')[0].strip()
            ports.append(port)

    # Create the nmap command
    ports_str = ','.join(ports)
    nmap_command = f"nmap -p {ports_str} -A -oN nmap/service -T5 {IP}"

    # Print the nmap command (for debugging purposes)
    print(f"Running nmap command: {nmap_command}")

    # Execute the nmap command
    os.system(nmap_command)

if __name__ == "__main__":
    main()
