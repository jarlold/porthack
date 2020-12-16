import sys
from pymetasploit3.msfrpc import MsfRpcClient

CVEs = sys.argv[1:]
print(CVEs[1])
client = MsfRpcClient('hacksh1337', ssl=False)

for CVE in CVEs:
    CVEl = CVE.lower()
    for exploit in client.modules.exploits:
        if CVEl in client.modules.use("exploit", exploit).description.lower():
            print("found")
        if CVEl in client.modules.use("exploit", exploit).modulename.lower():
            print("found")
        if CVEl in client.modules.use("exploit", exploit).references.lower():
            print("found")
        for ref in client.modules.use("exploit", exploit).references:
            if CVEl in ref.lower():
                print("found")
                

#print(client.modules.exploits[2])
#print(client.modules.exploits[2].__class__)
#print(dir(client.modules.exploits[2]))




