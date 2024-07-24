import requests
from win10toast import ToastNotifier
import webbrowser
import time
import threading

chainId = "ethereum"
pairAddress = "0x594daad7d77592a2b97b725a7ad59d7e188b5bfa"
is_honeypot_obj = {}

data = requests.get(f"https://api.dexscreener.com/latest/dex/pairs/{chainId}/{pairAddress}").text

def sendNotification(honeypot_obj, title, message, link):
    if not honeypot_obj.get("notify", False):
        return

    toaster = ToastNotifier()
    toaster.show_toast(title,
                message,
                icon_path=None,
                duration=10,
                threaded=True)
    
    def monitorNotification():
        while toaster.notification_active():
            time.sleep(0.1)
        if not toaster.notification_active():
            webbrowser.open(link)

    threading.Thread(target=monitorNotification).start()

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



if __name__ == "__main__":
    title = "Important Update Available"
    message = "Click here to download the latest version."
    link = f"https://www.dextools.io/app/en/ether/pair-explorer/{pairAddress}"
    isRug(pairAddress)
    print('\n\n', is_honeypot_obj) # for testing purposes 
    sendNotification(is_honeypot_obj, title, message, link)

# Look into dextools API
# Look into setting up desktop notifications and SMS notifications using sinch or pushover