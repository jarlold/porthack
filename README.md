# PortHack
A script to try a bunch of obvious steps in service exploitation, this script is very 'noisy' and probably
shouldn't be used on a system with any sort of IDS or ICE.

tl;dr<br>

<p align="center">
  <img src="./random_bullshit_go.png"/>
</p>


# What exactly does it do?
```
things with an `[X]` next to them are implemented
things without an `[X]` next to them are planned.

 -> Nmap vulners scan [X]
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
 -> If SSH [X]
    --> Try default SSH logins [X]
 -> If FTP
    --> Try default FTP logins
 -> If SQL
    --> Try default SQL logins
```

# Installation and Requirements
```
To install just clone the repo and run porthack.sh
The current requirements are:
    - searchsploit
    - nmap
    - metasploit framework
    - python2.7
           with pymetasploit 
           mechanize 
           paramiko 
    
These all need to be in your system path. (I.E /usr/bin/ or wherever else)!<br>
In future the python script will be compiled to executables before distribution,
but let me make the script not-useless before we bother with any of that, okay?
```
