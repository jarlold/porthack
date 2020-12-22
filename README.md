# PortHack
A script to try a bunch of obvious steps in service exploitation, this script is very 'noisy' and probably
shouldn't be used on a system with any sort of IDS or ICE.

tl;dr<br>
![random_bullshit](random_bullshit_go.png)

# What exactly does it do?
```
things with an `[X]` next to them are implemented
things without an `[X]` next to them are planned.

 -> Nmap vulners scan [X]
 -> put the CVEs into metasploit [X]
    --> bring up CVEs (selector menu?)
 -> put the CVEs into exploit_db command [X]
    --> bring up CVEs  (selector menu?)
 -> If port 80
    --> run SQLMap
    --> run wordpress hack
    --> detect router page?
        --> run router default logins
    --> detect login page
        --> offer to skip process
        --> run default logins
 -> If SSH
    --> Try default SSH logins
 -> If FTP
    --> Try default FTP logins
 -> If SQL
    --> Try default SQL logins
```
