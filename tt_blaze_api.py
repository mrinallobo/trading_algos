import requests
import json

BASE_URL = "https://ttblaze.iifl.com/apimarketdata"

headers = {
    "Content-Type": "application/json",
}

def login(secret_key, app_key, source):
    url = f"{BASE_URL}/auth/login"
    payload = {
        "secretKey": secret_key,
        "appKey": app_key,
        "source": source
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

def logout(token):
    url = f"{BASE_URL}/auth/logout"
    headers["Authorization"] = token
    response = requests.delete(url, headers=headers)
    return response.json()

def client_config(token):
    url = f"{BASE_URL}/config/clientConfig"
    headers["Authorization"] = token
    response = requests.get(url, headers=headers)
    return response.json()

def instruments_quotes(token, instruments, xts_message_code, publish_format):
    url = f"{BASE_URL}/instruments/quotes"
    headers["Authorization"] = token
    payload = {
        "instruments": instruments,
        "xtsMessageCode": xts_message_code,
        "publishFormat": publish_format
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

def instruments_subscription(token, instruments, xts_message_code):
    url = f"{BASE_URL}/instruments/subscription"
    headers["Authorization"] = token
    payload = {
        "instruments": instruments,
        "xtsMessageCode": xts_message_code
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

def instruments_unsubscription(token, instruments, xts_message_code):
    url = f"{BASE_URL}/instruments/subscription"
    headers["Authorization"] = token
    payload = {
        "instruments": instruments,
        "xtsMessageCode": xts_message_code
    }
    response = requests.put(url, headers=headers, data=json.dumps(payload))
    return response.json()

# Example usage
secret_key = "Sft@1111"
app_key = "3064470037e8c577"
source = "WebAPI"

login_response = login(secret_key, app_key, source)
token = login_response["result"]["token"]

# Perform other API calls using the token, for example:
client_config_response = client_config(token)
quotes_response = instruments_quotes(token, [{"exchangeSegment": 1, "instrumentID": 1000001}], 1502, "JSON")
subscription_response = instruments_subscription(token, [{"exchangeSegment": 1, "instrumentID": 1000001}], 1502)
unsubscription_response = instruments_unsubscription(token, [{"exchangeSegment": 1, "instrumentID": 1000001}], 1502)

# Logout
logout_response = logout(token)
