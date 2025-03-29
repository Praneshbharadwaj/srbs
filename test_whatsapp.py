import requests
import json

# Interakt API details
API_URL = "https://api.interakt.ai/v1/public/message/"
TOKEN = "OVpnSU95V1hUZmtkOFNOVWpObnlrQUNQYVV6MmZWdlpMX3AyUTFnWW9tczo="
PHONE_NUMBER = "8431664163"

def send_whatsapp_message():
    headers = {
        "Authorization": f"Basic {TOKEN}",
        "Content-Type": "application/json"
    }

    # payload = {
    #     "countryCode": "91",  # Example for India, change if needed
    #     "phoneNumber": PHONE_NUMBER,
    #     "callbackData": "test_callback",
    #     "type": "text",
    #     "text": "Hello! This is a test message from my WhatsApp Web API integration."
    # }

    payload = {

    "countryCode": "+91",

    "phoneNumber": "8431664163",

    # "campaignId" : "YOUR_CAMPAIGN_ID", 

    "callbackData": "some text here",

    "type": "Template",

    "template": {

        "name": "receipt",

        "languageCode": "en",

        "bodyValues": [

            "prathith",

            "108"

        ]

    }

}

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Failed to send message. Status code: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    send_whatsapp_message()
