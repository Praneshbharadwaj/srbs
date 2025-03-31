import requests
import json

# Interakt API details
API_URL = "https://api.interakt.ai/v1/public/message/"
TOKEN = "OVpnSU95V1hUZmtkOFNOVWpObnlrQUNQYVV6MmZWdlpMX3AyUTFnWW9tczo="  

def send_whatsapp_message(name, receipt_url, amount, phone,year,invitation_url):
    headers = {
        "Authorization": f"Basic {TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "countryCode": "+91",
        "phoneNumber": phone,
        "callbackData": "some text here",
        "type": "Template",
        "template": {
            "name": "receipt_var",
            "languageCode": "en",
            "bodyValues": [
                f"{name}",  # Single-line format
                f"Rupees {amount}",
                f"{year}",
                f"{receipt_url}",
                f"{invitation_url}"
            ]
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)