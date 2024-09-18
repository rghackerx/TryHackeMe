#madness #thm #easy #mindset #stegnography #privesc #screen  

-> commands 
	`rustscan -a 10.10.37.57 -r 1-65535 -- -A`
	`nmap -p- 10.10.37.57 -T4 -Pn -oN nmap.txt`
	
#### Ports
```
PORT      STATE    SERVICE
22/tcp    open     ssh
80/tcp    open     http
```

-> commands 
	`feroxbuster -u http://10.10.37.57/ -x txt,html,php,png,jpg,jpeg,zip,pcap,json`
#### Directory Enumeration
```
http://10.10.37.57/thm.jpg
http://10.10.37.57/
11320c http://10.10.37.57/index.php
```

-> the image was broken , so i used magicbytes tool to fix it 
-> `python3 magicbytes.py -i thm.jpg -m jpg`
-> got corrected image
-> image
![[Pasted image 20240919031400.png]]
-> hidden directory : */th1s_1s_h1dd3n*

#### Enumeration 

-> this page saying , tell me a secret and give hint that it would be in b/w 0-99
-> but i don't have any field to pass secret there , just a static page
-> after thinking for some seconds i though to pass an endpoint ?secret=?
-> no i made a python script to generate 0-99 num and then fuzzed it.

--> script.py
```python
with open('num.txt','w') as fyle:
for i in range(0,100):
fyle.writelines(str(i) + '\n')
```

-> `gobuster fuzz -u 'http://10.10.37.57/th1s_1s_h1dd3n/?secret=FUZZ' -w num.txt -t 64 --exclude-length 408`

-> found : 78 number is the correct secret value 
	[http://madness.thm/th1s_1s_h1dd3n/?secret=73]
-> got this : 
	*Urgh, you got it right! But I won't tell you who I am! **y2RPJ4QaPF!B***

-> let's find out what this sting is : **y2RPJ4QaPF!B**
-> in hint : ROTten guys name was mentioned , as i already think about ROT but don't know which one , as per the hint it's 10 
```
OG     : y2RPJ4QaPF!B
ROT 10 : i2BZT4AkZP!L  -> this might be the ssh uname??
```

##### uh , oh!! It's a rabbit hole

--> move back ! `steghide extract -sf thm.png`
-> pass : `y2RPJ4QaPF!B`
-> got a usename : wbxmr -> ROT13 -> `joker`

-> now i was sucked here for a long time , i saw a hint and get to know about the header image on this CTF THM Page , damn!!! unrealistic

-> `curl https://i.imgur.com/5iW7kC8.jpg -o 5iW7kC8.jpg`
-> `steghide extract -sf 5iW7kC8.jpg`  -> no pass needed
```
I didn't think you'd find me! Congratulations!

Here take my password

*axA&GF8dP
```

#### Gaining Shell

`ssh joker@madness.thm`
-> got user's shell

###### user.txt : ***THM{d5781e53b130efe2f94f9b0354a5e4ea}***

#### Privilege Escalations

-> `sudo -l` -> user not in sudoers file
-> `find / -type f -perm -u=s 2>/dev/null`
```
/bin/screen-4.5.0
```

-> here's a very famous exploit for this :
	https://www.exploit-db.com/exploits/41154

-> execute it step wise and got root shell
###### root.txt : ***THM{5ecd98aa66a6abb670184d7547c8124a}***

--- 

