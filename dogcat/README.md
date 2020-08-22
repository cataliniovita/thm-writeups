# 'dogcat' box writeup
## dogcat is a CTF box created by jammy and available on the [TryHackMe platform](https://tryhackme.com).
## Read about [LFI using wrappers](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/File%20Inclusion#wrapper-phpfilter)

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

+ **Let's understand this php code to see what's happening behind: 
We have a **containsStr** function which returns the first occurence of a substring in a string; it's like the C **strstr** function.
There's a **$ext** variable which will be used to set a specific extension: we saw before that every string that we insert will end by having a *php* extension.
First, the script checks if the view parameter is not NULL, then checks if the query string contains the cat or dog substrings. If this happens, we get the inclusion and simultanously the extension is set


