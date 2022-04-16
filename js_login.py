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
chrome_options.add_argument("--headless")
wd = ChromeDriverManager().install()
br = webdriver.Chrome(wd, options=chrome_options)


def find_login_elements(browser):
    pass


def try_credentials(username, password):
    pass


# Will take a string of HTML and try to determine if it's a successful login page
# Returns false if failure, returns True if not-failure
def is_page_login_success(page, original_page):
    for i in login_failure_keywords:
        if i in page and not i in original_page:
            return False
    return True


# Checks if the response verification we're using we'll work on this page
# (Checks if is_page_login_success actually works on this site)
# Will return True if the function works correctly, will return False otherwise
def verify_success_function(login_form, username_control, password_control, original_page):
    br.form = login_form # select the login form
    res = try_username_password(br, username_control, password_control, 'asdlkjwial', 'safeakj')
    return not is_page_login_success(res, original_page)





