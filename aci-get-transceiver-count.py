
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

count_dict = {}
# Initialize an empty dictionary to store the counts of unique values
count_dict = {}

# Iterate through the data and count the occurrences of each unique value
for item in inv:
    guiCiscoEID = item['ethpmFcot']['attributes']['guiCiscoEID']
    if guiCiscoEID in count_dict and item['ethpmFcot']['attributes']['state'] == 'inserted':
        count_dict[guiCiscoEID] += 1
    else:
        count_dict[guiCiscoEID] = 1


filtered_data = {key: value for key, value in count_dict.items() if value != 1}

print(filtered_data)
