# 'dogcat' box writeup
## dogcat is a CTF box created by jammy and available on the [TryHackMe platform](https://tryhackme.com).
## Read about

# ![bg](images/background.png?raw=true "Title")

## Foothold
+ **We deploy the machine and start with a nmap scan for open ports**

``nmap -sV -sC -oN scan1 10.10.23.37``

+ **We observe 2 open ports, ssh and an http, the last one with an Apache service**

# ![h](images/nmapp.jpg?raw=true "dog")
