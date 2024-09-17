import json
import requests

#ed69d93a-8e89-452d-a3b4-f430a6ec2f2e
#NDFhYzYxNGItMzYxMy00ZDhkLTg2ZjQtMzZiZjcyOTJiMTYwOmVkNjlkOTNhLThlODktNDUyZC1hM2I0LWY0MzBhNmVjMmYyZQ==

def get_gigachat_token():
    # Get token
    token_url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
    token_headers = {
        'Authorization': 'Basic NDFhYzYxNGItMzYxMy00ZDhkLTg2ZjQtMzZiZjcyOTJiMTYwOmVkNjlkOTNhLThlODktNDUyZC1hM2I0LWY0MzBhNmVjMmYyZQ==',
        'RqUID': '41ac614b-3613-4d8d-86f4-36bf7292b160',
        'Content-Type': 'application/x-www-form-urlencoded',
        "scope": 'scope=GIGACHAT_API_PERS'
    }
    token_data = 'scope=GIGACHAT_API_PERS'
    token_response = requests.post(token_url, headers=token_headers, data=token_data, verify=False)
    token = token_response.json()['access_token']
    return token

def do_request(messages):
    token = get_gigachat_token()
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    payload = json.dumps({
        "model": "GigaChat:latest",
        "messages": messages,
        "temperature": 0.87,
        "top_p": 0.47,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1.07,
        "update_interval": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    return json.loads(response.text)['choices'][0]['message']['content']