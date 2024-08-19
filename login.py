from fbchat import Client
import json

def login_to_facebook():
    try:
        with open("appstate.json", "r") as f:
            session = json.load(f)
            client = Client(None, None, session_cookies=session)
    except (FileNotFoundError, Exception):
        email = "email@example.com"
        password = "your_password"
        client = Client(email, password)
        with open("appstate.json", "w") as f:
            f.write(json.dumps(client.getSession()))
    return client
