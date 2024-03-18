import time
import requests
import json
import datetime
from datetime import datetime, timedelta

# Replace with your actual APIC and credentials
user_apic = 'apic#local' + "\\" + "\\" + 'USERNAME'
password_apic = "PASSWORD"
apic_ip = "APICIP"

# Filter out the new faults, assuming 'new' is defined by some criteria
url = "https://{}/api/node/class/faultInfo.json?query-target-filter=and(ne(faultInfo.severity,%22cleared%22),eq(faultInst.ack,%22no%22),eq(faultDelegate.ack,%22no%22))"

# Disable warnings for unverified HTTPS requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


# Function for get APIC Token
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


def send_to_telegram(message):
    # Replace with your telegram token and chat id
    apiToken = 'TELEGRAM_API_TOKEN'
    chatID = '-CHATID'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

while True:
    # Get the current date and delta for 2 minutes
    current_datetime = datetime.now()
    current_datetime_diff = current_datetime - timedelta(minutes=2)
# Perform the request to the APIC
    try:
        token = GetAPICToken(apic_ip, user_apic, password_apic)

        response = requests.get(url.format(apic_ip), headers=token ,verify=False)

        # Check if response is successful
        if response.status_code == 200:
            faults = response.json()['imdata']
            #print(faults)

            for x in faults:

                created_date_time = datetime.strptime(x[list(x.keys())[0]]['attributes']['created'][0:19], '%Y-%m-%dT%H:%M:%S')
                if created_date_time > current_datetime_diff:
                    #print(x)
                    final_res = ""
                    final_res += "Created: " + x['faultInst']['attributes']['created'] + '\n'
                    final_res += "LastTransition: " + x['faultInst']['attributes']['lastTransition'] + '\n'
                    final_res += "Cause: " + x['faultInst']['attributes']['cause'] + '\n'
                    final_res += "Status: " + x['faultInst']['attributes']['status'] + '\n'
                    final_res += "LC Status: " + x['faultInst']['attributes']['lc'] + '\n'
                    final_res += "Occur: " + x['faultInst']['attributes']['occur'] + '\n'
                    final_res += "ChangeSet: " + x['faultInst']['attributes']['changeSet'] + '\n'
                    final_res += "Description: " + x['faultInst']['attributes']['descr'] + '\n'
                    final_res += "Subject: " + x['faultInst']['attributes']['subject'] + '\n'
                    final_res += "DN: " + x['faultInst']['attributes']['dn'] + '\n'
                    final_res += "Domain: " + x['faultInst']['attributes']['domain'] + '\n'
                    final_res += "Rule: " + x['faultInst']['attributes']['rule'] + '\n'
                    final_res += "Fault Code: " + x['faultInst']['attributes']['code'] + '\n'
                    send_to_telegram(final_res)


        else:
            send_to_telegram(f"Failed to fetch faults. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        send_to_telegram(f"An error occurred: {e}")
    time.sleep(90)
