import mechanize
from sys import argv
from random import choice
import re
import ssl

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

# Like above but for determining if a page is a failed login or a successful login
login_failure_keywords = ["incorrect", "login failed", "invalid"]

# Load in the list of default username and passwords to try out
with open("default_passwords.txt", 'r') as opn:
    default_passwords = opn.readlines()

# The main browser object, used everywhere so it gets to be up here
br = mechanize.Browser()


# Will find a form with 2 controls and a username prompt or 2 controls and a password prompt
# In the event of a double-match will prioritize the last form over the first one
def find_login_form(br): 
    login_form = None
    username_control = None
    password_control = None

    for l in br.forms(): 
        for i in l.controls: 
            for k in username_keywords: 
                if (i.name and k in i.name) or (i.id and k in i.id): # IS TO GO
                    login_form = l 
                    username_control = i 

            for k in password_keywords:
                if (i.name and k in i.name) or (i.id and k in i.id) and not k == username_control:
                    login_form = l
                    password_control = i
    if login_form:
        return login_form, username_control, password_control


# Assuming a form is already selected, will try a username and password combination and return the result.
# Will also read the page, and remove the username and password from the page
def try_username_password(br, user_control, pass_control, username, password):
    br[str(user_control.name)] = username
    br[str(pass_control.name)] = password
    return br.submit().read().replace(username, '').replace(password, '')


# Will take a string of HTML and try to determine if it's a successful login page
# Returns false if failure, returns True if not-failure
def is_page_login_success(page, original_page):
    for i in login_failure_keywords:
        if i in page and not i in original_page:
            return False
    return True


# Try all the passwords lol
def try_all_passwords(login_form, username_control, password_control, original_page):
    login_responses = []
    for i in default_passwords:
        # Parse the password from the file
        i = i.strip().strip("\n")
        username, password = i.split(" ") if len(i.split(" ")) == 2 else (i, "")

        # Try the username + password combo
        br.form = login_form # reselect the form each time
        res = try_username_password(br, username_control, password_control, username, password)

        # If the result doesn't look too much like a failure, log it!
        if is_page_login_success(res, original_page):
            login_responses.append( (username, password, res) )
    return login_responses


# Checks if the response verification we're using we'll work on this page
# (Checks if is_page_login_success actually works on this site)
# Will return True if the function works correctly, will return False otherwise
def verify_success_function(login_form, username_control, password_control, original_page):
    br.form = login_form # select the login form
    res = try_username_password(br, username_control, password_control, 'asdlkjwial', 'safeakj')
    return not is_page_login_success(res, original_page)


def main():
    # Disables SSL verificaton, this is a security risk and makes the script vulernable to MiTM and false-host
    # attacks
    ssl._create_default_https_context = ssl._create_unverified_context

    # Change some settings so it's not super-clear that we're an automated script.
    br.set_handle_robots(False)

    # Finally open up the webpage
    original_page = br.open(url)

    # Find the form and select it in the browser
    login_form, username_control, password_control = find_login_form(br)
    br.form = login_form

    # Check to see if we're able to tell apart failed and succesful logins
    if not verify_success_function(login_form, username_control, password_control, original_page):
        print("Unable to tell apart login successes and failures, skipping default password test.")
        exit()

    # Try all the default passwords
    print("Trying default_passwords.txt on website login...")
    login_responses = try_all_passwords(login_form, username_control, password_control, original_page)

    # Print possible valid logins
    print("The following usernames + passwords *MAY* be valid:")
    for i in login_responses:
        print("  --> " + i[0] + " " + i[1])

if __name__ == "__main__":
    main()
