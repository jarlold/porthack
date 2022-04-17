import ftplib
from sys import argv
from sys import stdout
from time import sleep
import _socket

# Loads in the host IP address provided through stdin
ip = str(argv[1])
port = 21

# Load in the list of usernames + passwords to test
# We'll use the same username and passwords as SSH.
opn = open('wordlists/default_ssh.txt', 'r')
default_logins = [ i.strip() for i in opn.readlines() ]
opn.close()

# We'll store the possibly valid credentials in here
valid_logins = []

# Setup the FTP connection
client = ftplib.FTP()

# Test a login, we'll kill and restart the connection each time
# this is to avoid certain session timeout errors.
def attempt_login(username, password, timeout=30):
    try:
        #ftplib.FTP(ip, timeout=timeout)
        client.connect(ip, port, timeout=timeout)
        client.login(username, password)
        client.quit()
        return True
    except ftplib.error_perm as e:
        client.quit()
        return False
#   except ConnectionRefusedError as e:
#       print("Unable to connect to FTP on port 21")
#       exit()
    except KeyboardInterrupt as e:
        print("Quiting..")
        exit()
    except _socket.gaierror as e:
        print(e)
        exit()
    except OSError as e:
        print(e)
        exit()
#   except Exception as e:
#       print("Unkown exception")
#       return None

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
print("Trying common FTP creds on port " + str(port) + "...")

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
        print("  --> " + str(i))
else:
    print("  --> None :c")
