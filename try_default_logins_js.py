from sys import argv
from random import choice
import re
import ssl
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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
chrome_options = Options()
#chrome_options.add_argument("--headless")
wd = ChromeDriverManager().install()
br = webdriver.Chrome(wd, options=chrome_options)


# Will find a form with 2 controls and a username prompt or 2 controls and a password prompt
# In the event of a double-match will prioritize the last form over the first one
def find_login_form(br): 
    username_control = None
    password_control = None
    submit_button = None;

    for i in br.find_elements_by_tag_name("input"):
        name = i.get_property("name").lower() if not i.get_property("name") is None else None
        for k in username_keywords: 
            if (i.id and k in i.id.lower()) or (k in name): # IS TO GO
                username_control = i

        for k in password_keywords:
            if (i.id and k in i.id.lower()) or (name and k in name) and not k == username_control:
                password_control = i
    
    for i in br.find_elements_by_xpath("//*login*"):
        for k in submit_keywords:
            if (i.id and k in i.id.lower()) or (name and k in name) and not k == username_control and not k==password_control:
                submit_button = i
            
    return username_control, password_control


# Assuming a form is already selected, will try a username and password combination and return the result.
# Will also read the page, and remove the username and password from the page
def try_username_password(br, user_control, pass_control, username, password):
    user_control.send_keys(username)
    pass_control.send_keys(password)
    pass_control.submit()
    exit()
    return br.page_source.replace(username, '').replace(password, '')


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
def verify_success_function(username_control, password_control, original_page):
    res = try_username_password(br, username_control, password_control, 'asdlkjwial', 'safeakj')
    return not is_page_login_success(res, original_page)


def main():
    # Finally open up the webpage
    print(url)
    original_page = br.get(url)

    # Find the form and select it in the browser
    username_control, password_control = find_login_form(br)

    # If no login form, username control, or password was found, then this probably isn't a log-in page
    if not username_control or not password_control:
        directory = url.split("/")[-1] if not url[-1] == "/" else "/"
        print("No login form found, skipping {} because it's probably not a login page.".format(directory))

    # Check to see if we're able to tell apart failed and succesful logins
    if not verify_success_function(username_control, password_control, original_page):
        print("Unable to tell apart login successes and failures, skipping default password test.")
        exit()

    # Try all the default passwords
    print("Trying default_passwords.txt on website login...")
    login_responses = try_all_passwords(login_form, username_control, password_control, original_page)

    # Print possible valid logins
    print("The following usernames + passwords *MAY* be valid:")
    if not len(login_responses) == 0:
        for i in login_responses:
            print("  --> " + i[0] + " " + i[1])
    else:
        print(" --> None :c")


if __name__ == "__main__":
    main()
