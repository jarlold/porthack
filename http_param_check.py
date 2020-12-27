import mechanize
from sys import argv
from random import choice
import re
import ssl


# Detect login HTML form
# Use an unlikely username + password to find what failed login looks like
# Try the default_passwords.txt list
# --> If the return - (username + password) - (attempts remaining #) matches the failed login, try again
# --> Otherwise report the result to the user, and ask if the testing should continue

url = argv[1]

user_agent = [
    'Mozilla/5.0 (X11; U; Linux; i686; en-US; rv:1.6) Gecko Debian/1.6-7',
    'Konqueror/3.0-rc4; (Konqueror/3.0-rc4; i686 Linux;;datecode)',
    'Opera/9.52 (X11; Linux i686; U; en)'
    ]

# Case insensitive list of words that will cause an <input> tag to be flagged as either a username prompt
# or a password prompt.
username_keywords = ["username", "name"]
password_keywords = ["password"]


def find_form_elements(page): # there's a nicer regex out there...
    return re.findall("<input[^\/>]{1,}id=[^\/>]{1,}\/>", page)


# Disables SSL verificaton, this is a security risk and makes the script vulernable to MiTM and false-host
# attacks.
ssl._create_default_https_context = ssl._create_unverified_context

# Change some settings so it's not super-clear that we're an automated script.
br = mechanize.Browser()
br.set_handle_robots(False)
#br.addheaders = [('User-agent:', choice(user_agent))]

# Finally open up with webpage
r = br.open(url)

# Search it for a login prompt of some sort
forms = find_form_elements(r.read())
username_forms = list() # Find the usernames
for i in forms:
    for k in username_keywords:
        if k.lower() in i.lower():
           username_forms.append(i)

password_forms = list() # Find the passwords
for i in forms:
    for k in password_keywords:
        if k.lower() in i.lower():
            password_forms.append(i)

print("username:")
for i in username_forms: print(i)
print("passwords:")
for i in password_forms: print(i)

id = re.findall("name=[^ ]{1,}\s", username_forms[0])[0].strip().replace("\"", '')[5:]
print(id)
br.select_form(name="name")
