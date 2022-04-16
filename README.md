# PortHack
A script to try a bunch of obvious steps in service exploitation, this script is very 'noisy' and probably
shouldn't be used on a system with any sort of IDS or ICE. The goal of this script is to get as far as possible
into the exploitation process without user input.

tl;dr<br>

<p align="center">
  <img src="./random_bullshit_go.png"/>
</p>


# What exactly does it do?
```
things with an `[X]` next to them are implemented
things without an `[X]` next to them are planned.

 -> Nmap vulners scan [X]
    --> Regex and cache which services are on which ports.
 -> put the CVEs into metasploit [X]
    --> bring up CVEs (selector menu?)
 -> If port 80 [X]
    --> run SQLMap
    --> run wordpress hack
    --> detect router page?
        --> run router exploit
    --> detect login page [X]
        --> offer to skip process
        --> run default logins [X]
 -> If port 22 [X]
    --> Try default SSH logins [X]
 -> If port 21
    --> Try default FTP logins [X]
 -> If port 3306
    --> Try default SQL logins
```

Currently the program revolves around default-ports, obviously this isn't
ideal, and it should go through a brief recon step of figuring out which services
are on what ports.

# Installation and Requirements
```
To install just clone the repo and run porthack.sh
The current requirements are:
    - searchsploit
    - nmap
    - metasploit framework
    - python3.x
           with pymetasploit 
           mechanize 
           paramiko 
    
These all need to be in your system path. (I.E /usr/bin/ or wherever else)!<br>
In future the python script will be compiled to executables before distribution,
but let me make the script not-useless before we bother with any of that, okay?
```
