import requests
from winotify import Notification, audio

chainId = "ethereum"
pairAddress = "0xd7570342c2d5de4413ec131b5e79c4aeeef5d35d"
is_honeypot_obj = {}

data = requests.get(f"https://api.dexscreener.com/latest/dex/pairs/{chainId}/{pairAddress}").text

def sendNotification(honeypot_obj):
    if honeypot_obj["notify"] == False:
        return False
    notification_popup = Notification(app_id="Dextools trending notifier",
                                      title="New token",
                                      duration="long",
                                      icon="")
    notification_popup.add_actions(label="Launch chart", launch=f"https://www.dextools.io/app/en/ether/pair-explorer/{pairAddress}")
    # TO-DO - send desktop and sms notification

def isRug(address):
    url = "https://api.honeypot.is/v2/IsHoneypot"

    params = {
        "address": address
    }
    honeypot_response = requests.get(url, params = params)
    for key, value in honeypot_response.json().items():
        if key == "summary":
            if value["risk"] == 'medium' or value["riskLevel"] <= 31:
                is_honeypot_obj["notify"] = True
            if value["risk"] == 'low' or value["riskLevel"] <= 31:
                is_honeypot_obj["notify"] = True
            else:
                is_honeypot_obj["notify"] = False

        if key == "honeypotResult":
            if value["isHoneypot"] == True:
                is_honeypot_obj["notify"] = False

        if key == "simulationResult" and value["buyTax"] != 0 and value["sellTax"] != 0 and value["transferTax"] != 0 and value["buyGas"] != 0 and value["sellGas"] != 0:
            is_honeypot_obj["notify"] = False
        
        if key == "flags":
            if "EXTREMELY_HIGH_TAXES" in value or "high_fail_rate" in value or "some_snipers_honeypot" in value:
                is_honeypot_obj["notify"] = False
        print(key, ' : ', value)


isRug(pairAddress)

# Look into dextools API
# Look into setting up desktop notifications and SMS notifications using sinch or pushover