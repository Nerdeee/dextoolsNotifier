import requests

chainId = "ethereum"
pairAddress = "0x0542c51aaf23f13e9f0f11accda67b06ae561a4c"

data = requests.get(f"https://api.dexscreener.com/latest/dex/pairs/{chainId}/{pairAddress}").text

def isRug(address):
    url = "https://api.honeypot.is/v2/IsHoneypot"

    params = {
        "address": address
    }
    honeypot_response = requests.get(url, params = params)
    print(honeypot_response.json())

isRug(pairAddress)

# need to add logic for rug check + look into dextools API
# Look into setting up desktop notifications and SMS notifications using sinch or pushover