import requests

def send_sms(to_number, message):
    print("number",str(to_number))
    url = "https://www.fast2sms.com/dev/bulkV2"
    headers = {
        "authorization": "ouOzhifNrUdm85SZ3ajl2GIeVYcT0HEJR9gXbp6P1CBFq4QyLDfhRVuz7FkeZ94mcS3qy0MAIH6KLdsl",  # Replace with actual API key
        "Content-Type": "application/json"
    }
    payload = {
        "route": "q",
        "message": message,
        "flash": 0,
        "numbers": str(to_number)  # Ensure this is a valid mobile number
    }

    response = requests.post(url, headers=headers, json=payload)

    print("Raw Response:", response.text)  # Debugging
    try:
        print("Response JSON:", response.json())  
    except requests.exceptions.JSONDecodeError:
        print("Error: Invalid JSON response from Fast2SMS")


