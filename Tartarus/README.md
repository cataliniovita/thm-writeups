# 'Tartarus' box writeup
## Tartarus is a CTF box created by csenox and available on the [TryHackMe platform](https://tryhackme.com).
## Read about
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

+ **The files looks like some login credentails so let's use them to bruteforce our login page found. I'm gonna use hydra for this, but first i'm gonna see the login request form needed for our bruteforce tool**

# ![8](images/burprealreq.jpg?raw=true "req")

**It seems we have a post form, and the 'Incorrect username' as failure condition we're gonna use for the hydra. But surely there's another failure condition, maybe an 'Incorrect password' one, which we need too, because hydra will only parse the user's list and will take all passwords as good. So, we're gonna use the help of a regex to create the failure condition, which will be ``Incorrect*``**

``hydra 10.10.3.149 -L userid -P credentials.txt http-post-form "/sUp3r-s3cr3t/authenticate.php/:username=^USER^&password=^PASS^&Login=Login:F=Incorrect*"``

# ![9](images/hydrated.jpg?raw=true "hydr")

+ **Using the credentials to login on our page, we can see we have an upload section, so let's try to uploada php reverse shell**





`





