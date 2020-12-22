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

# Check for
# -> Nmap vulners scan [X]
# -> put the CVEs into metasploit [X]
#    --> bring up CVEs (selector menu?)
# -> If port 80
#    --> run SQLMap
#    --> run wordpress hack
#    --> detect router page?
#        --> run router default logins
#    --> detect login page
#        --> offer to skip process
#        --> run default logins
# -> If SSH
#    --> Try default SSH logins
# -> If FTP
#    --> Try default FTP logins
# -> If SQL
#    --> Try default SQL logins



# Uses the nmap "vulners.nse" vulnerability detection script
echo "Doing nmap vulnerability scan..."
scan1=$(nmap -sV --script vulners $1)


# Find and count the number of CVEs
CVEs=$(echo ${scan1}  | grep --only-matching 'CVE-....-.....') # not sure if this counts *ever* CVE format
NumCVEs=$(echo ${CVEs} | grep --only-matching "CVE" | wc -l)
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

