import os
from sys import argv
from metasploit.msfrpc import MsfRpcClient
from metasploit.msfconsole import MsfRpcConsole
import time
import re

# Get the list of CVEs from STDIN
CVEs = argv[1:]


# These variables will hold the output of the console after command executions
global global_positive_out
global_positive_out = list()
global global_console_status
global_console_status = False


# The callback function that sets the above variables after client.execute 
# Not gonna lie, copied this from stack overflow- but it's pretty simple
# Edit: this isn't the exact code from stack overflow anymore, it's a simplified
# version
def read_console(console_data):
#    global global_console_status
#    global_console_status = console_data['busy']
    sigdata = console_data['data'].rstrip().split('\n')
    for line in sigdata:
        global_positive_out.append(line)
    global global_console_status
    global_console_status = False

# Clears the console, it's mainly wrapped to make updating it easier in the future
def clear_console():
    global global_positive_out
    global_positive_out = list()

# Creates the client object
client = MsfRpcClient("hacksh1337", ssl=False)
    
# Create the conso
console = MsfRpcConsole(client, cb=read_console)

# Find all the msfmodules relating to each CVE
def search_for_cve(cve):
    clear_console()
    global global_console_status
    global_console_status = True
    console.execute("search cve:{}".format(cve))
    while global_console_status:
        time.sleep(1)
    return global_positive_out

# Cleans out CVE data from search_for_cve, to only include the path (I.E exploit/windows/smb/ms17_010...) of exploits
# because an automatic script can't really use auxilary or scanner modules without a lot of pre-coding -\(-_-)/-
def clean_cve_search(search_result):
    nl = list()
    for i in search_result:
        if "exploit/" in i and not "Interact with a module by name or index." in i:
            nl.append(i.split()[1])
    return nl

# Search for each CVE and record it in a list
cve_data = list()
for i in CVEs:
    cve_data += clean_cve_search(search_for_cve(i))


# Print out the CVE data 
for i in cve_data:
    print(" --> " + i)

# For some reason this is nessasary, mabye a hanging thread in a library or something
# oh well sucks to be that thread, get rekt nerd
os._exit(0)
