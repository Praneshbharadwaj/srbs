import requests
import base64

def send_whatsapp_with_local_file(name, phone, amount, receipt_url):
    # Remove any whitespace or newlines from the API key
    API_KEY = "OVpnSU95V1hUZmtkOFNOVWpObnlrQUNQYVV6MmZWdlpMX3AyUTFnWW9tczo=".strip()  
    
    # Correct encoding - add colon after API key before encoding
    encoded_api_key = base64.b64encode(f"{API_KEY}:".encode()).decode()
    
    url = "https://api.interakt.ai/v1/public/message/"

    message_text = f"""|| Sri Rama Bhaktha Sabha ||
Received with thanks from Smt/Sri {name} an amount of rupees {amount} towards 119th year Ramothsavam celebrations.
Thank you for your generous contribution towards seva of Lord Rama.
Receipt link: {receipt_url}
Programme list link: https://drive.google.com/file/d/1i-XBTJx0kLYWnp2ARjUIZ2-VHgeX_cvf/view?usp=drive_link"""

    payload = {
        "receiver": phone,
        "type": "template",
        "template_name": "document_message",
        "language": "en",
        "header": {
            "format": "document",
            "document": {
                "url": receipt_url,
                "filename": f"{name}_receipt.png"
            }
        },
        "body": {
            "text": message_text
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_api_key}"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.status_code, response.text)  # More detailed debug info

send_whatsapp_with_local_file(
    name="Pranesh",
    phone="918431664163",  # Added India country code 91
    amount="500",
    receipt_url="https://res.cloudinary.com/di30awmhx/image/upload/v1743186287/bktnsdhp2xtwbekvrzoz.png"
)