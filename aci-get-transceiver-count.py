
import requests
import json

#Replace with your credentials
user_apic = 'USERNAME'
password_apic = "PASSWORD"

#Reaplce with your APIC IP address
apic_ip = "APIC_IP"


url = "https://{}/api/class/ethpmFcot.json"

# Disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)



def GetAPICToken(apicip, user, password):
    json_input_auth = """{ "aaaUser" : { "attributes" : { "name" : "%s", "pwd" : "%s" } } }"""% (user, password)

    r_auth = requests.post('https://{}/api/aaaLogin.json'.format(apicip), json=eval(json_input_auth), verify=False)

    r_auth = r_auth.json()
    token = r_auth['imdata'][0]['aaaLogin']['attributes']['token']

    headers_apic = {
        "Cookie": f"APIC-Cookie={{}}".format(token)
    }
    return headers_apic
#


token = GetAPICToken(apic_ip, user_apic, password_apic)

response = requests.get(url.format(apic_ip), headers=token ,verify=False)

if response.status_code == 200:
    inv = response.json()['imdata']
    #print(inv)

# Initialize an empty dictionary to store the counts of unique values
count_dict = {}

for item in inv:
    guiCiscoEID = item['ethpmFcot']['attributes']['guiCiscoEID']
    if item['ethpmFcot']['attributes']['state'] == 'inserted':
        if guiCiscoEID in count_dict:
            count_dict[guiCiscoEID] += 1
        else:
            count_dict[guiCiscoEID] = 1

print(count_dict)
