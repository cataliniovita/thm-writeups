# 'Dav' box writeup
## Dav is a CTF box created by stuxnet and available on the [TryHackMe platform](https://tryhackme.com).
## Read about [WebDAV](https://en.wikipedia.org/wiki/WebDAV) and [Dav default credentials](http://xforeveryman.blogspot.com/2012/01/helper-webdav-xampp-173-default.html)
# ![bg](images/background.jpeg?raw=true "Title")

## Foothold
+ **We deploy the machine and start with a nmap scan for open ports**

``nmap -sV -sC -oN scan1 10.10.62.166``

+ **From our result, we can see that the 80 port is open, which is running an Appache with a default page**

# ![nmap](images/nmap_dirb_scan.jpg?raw=true "nmap")

+ **Let's run a gobuster search too and see our results. It seems that a webdav service is runnning**

``gobuster dir -u http://10.10.62.166/ -w /usr/share/wordlists/dirb/common.txt``

# ![dirb](images/nmap_dirb_scan2.jpg?raw=true "dirb")

**





