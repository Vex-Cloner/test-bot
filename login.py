from fbchat import Client
import json
import fbchat

def login_to_facebook():
    try:
        with open("appstate.json", "r") as f:
            session = json.load(f)
            client = Client(None, None, session_cookies=session)
    except (FileNotFoundError, Exception):
        email = "fixxyktimoh@uma3.be"
        password = "Nota3210@#"
        try:
            client = Client(email, password)
        except fbchat.FBchatUserError as e:
            print(f"Failed to log in: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
        with open("appstate.json", "w") as f:
            f.write(json.dumps(client.getSession()))
    return client
