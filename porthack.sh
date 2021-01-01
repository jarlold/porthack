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
# -> If SSH
#    --> Try default SSH logins
# -> If FTP
#    --> Try default FTP logins
# -> If SQL
#    --> Try default SQL logins


# Uses the nmap "vulners.nse" vulnerability detection script
echo "Doing nmap vulnerability scan..."
scan1=$(nmap -sV --script vulners $1)
echo "  --> done!"
echo

# Use some regex headaches to just find the services
services="""$(echo "$scan1" | egrep --only-matching "([0-9]{1,5})\/...\s{1,20}\w{4,9}\s{1,20}\w{1,30}")"""
echo "Found the following services:"
for i in ${services// /_} # look i'm not a bash programmer...
do
    echo "  --> ${i//_/ }" # trying to split this string was _weird_
done
echo

# Find and count the number of CVEs
CVEs=$(echo ${scan1}  | grep --only-matching 'CVE-....-.....') # not actually sure if this counts *every* CVE format
NumCVEs=$(echo ${CVEs} | grep --only-matching "CVE" | wc -l)
echo "And the following number of CVEs:"
echo "  --> found ${NumCVEs} CVEs"
echo


# Move this to the help text later I guess
#echo "Make sure msfrpcd is started, and is using the password specified"
#echo "if you don't know how to start it, or the password isn't right, just run"
#echo "msfrpcd -P hacksh1337 -S in a different terminal window, and leave it open"
#echo

# Runs a Python script to search for CVEs from Metasploit Framework
echo "Searching Metasploit framework for CVE scripts..."
msf_cves=$(python2 msf_cve_search.py $CVEs)
for i in ${msf_cves}
do
    echo "  --> ${i}"
done
echo 

# Check if http is listed in the services from the nmap scan
is_http=$(echo $services | grep --only-matching "80/tcp")

# If so, run a script to try a bunch of default usernames and passwords on it
if [ "${is_http}" == "80/tcp" ]
then
    python2 ./try_default_logins.py http://$1/
fi
