import os
import importlib.util
import json
import sqlite3
from fbchat import Client
from login import login_to_facebook

with open("config.json", "r") as f:
    config = json.load(f)

COMMAND_PREFIX = config["command_prefix"]
ADMIN_UID = config["admin_uid"]

def setup_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            uid TEXT PRIMARY KEY
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(uid):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('INSERT OR IGNORE INTO users (uid) VALUES (?)', (uid,))
    
    conn.commit()
    conn.close()

def is_user_registered(uid):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute('SELECT 1 FROM users WHERE uid = ?', (uid,))
    result = c.fetchone()
    
    conn.close()
    return result is not None

def load_command(command_name):
    command_file = f"scripts/cmds/{command_name}.py"
    if os.path.exists(command_file):
        spec = importlib.util.spec_from_file_location(command_name, command_file)
        command_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(command_module)
        if hasattr(command_module, "run"):
            return command_module.run()
        else:
            return f"The command `{command_name}` is missing a 'run()' function."
    else:
        return f"The command `{command_name}` doesn't exist."

class BotClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        setup_database()

    def onMessage(self, author_id, message, thread_id, **kwargs):
        if not is_user_registered(author_id):
            add_user(author_id)
        
        if message.text.startswith(COMMAND_PREFIX):
            command = message.text[len(COMMAND_PREFIX):].split(' ')[0]
            response = load_command(command)
            if response:
                self.send(message=response, thread_id=thread_id)
        if author_id == ADMIN_UID:
            if message.text == f"{COMMAND_PREFIX}shutdown":
                self.send(message="Shutting down...", thread_id=thread_id)
                self.logout()

if __name__ == "__main__":
    bot_client = login_to_facebook()
    if bot_client:
        bot_client.startListening()
