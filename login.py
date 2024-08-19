from fbchat import Client
import json

def login_to_facebook():
    with open("config.json", "r") as f:
        config = json.load(f)
    
    email = config["email"]
    password = config["password"]
    
    try:
        client = Client(email, password)
    except fbchat.FBchatUserError as e:
        print(f"Failed to log in: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    
    return client
