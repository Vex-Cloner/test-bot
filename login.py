import requests
import re
from fbchat import Client

def validate_cookie(cookie):
    headers = {
        'Accept-Language': 'id,en;q=0.9',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Referer': 'https://www.instagram.com/',
        'Host': 'www.facebook.com',
        'Sec-Fetch-Mode': 'cors',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Sec-Fetch-Site': 'cross-site',
        'Sec-Fetch-Dest': 'empty',
        'Origin': 'https://www.instagram.com',
        'Accept-Encoding': 'gzip, deflate',
    }
    
    response = requests.get(
        'https://www.facebook.com/x/oauth/status?client_id=124024574287414&wants_cookie_data=true&origin=1&input_token=&sdk=joey&redirect_uri=https://www.instagram.com/brutalid_/',
        headers=headers,
        cookies={'cookie': cookie}
    )
    
    if '"access_token":' in response.text:
        return True
    return False

def login_to_facebook():
    cookie = input("Please enter your Facebook cookie: ")
    
    if validate_cookie(cookie):
        client = Client(cookie=cookie)
        print("Logged in successfully using cookie.")
        return client
    else:
        print("Invalid cookie.")
        return None

if __name__ == "__main__":
    login_to_facebook()
