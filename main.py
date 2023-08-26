import subprocess
import re
import socket
from colorama import init, Fore
import time
import os

init(autoreset=True)

while True:
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
    netstat_output = subprocess.check_output(['netstat', '-ano'], universal_newlines=True)

    netstat_lines = netstat_output.splitlines()

    connections_info = []

    for line in netstat_lines[4:]:
        columns = line.split()
        if len(columns) >= 5:
            proto = columns[0]
            local_address = columns[1]
            foreign_address = columns[2]
            state = columns[3]
            pid = columns[4]

            if any(foreign_address.startswith(ip_start) for ip_start in ['0.0.0.0', '127.0.0.1', '[::]', '*:*']):
                continue

            connections_info.append((proto, local_address, foreign_address, state, pid))

    for proto, local_address, foreign_address, state, pid in connections_info:
        ip, port = foreign_address.rsplit(':', 1)

        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
        except socket.herror:
            hostname = "N/A"

        if hostname == "N/A":
            colored_hostname = hostname
        else:
            clean_hostname = re.sub(r'\033\[[0-9;]*m', '', hostname)
            clean_hostname = re.sub(r'\033\[.*?m', '', clean_hostname)  
            colored_hostname = Fore.RED + clean_hostname

        print(f"IP: {ip}\tPort: {port}\tHostname: {colored_hostname}\tPID: {pid}")
    time.sleep(5)

      
    
