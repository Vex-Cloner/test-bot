import os
import importlib.util
from fbchat import Client
from login import login_to_facebook

COMMAND_PREFIX = "!"

client = login_to_facebook()

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

@client.listen
def on_message(author_id, message):
    if message.text.startswith(COMMAND_PREFIX):
        command = message.text[len(COMMAND_PREFIX):].split(' ')[0]
        response = load_command(command)
        if response:
            client.send(message=response, thread_id=message.thread_id)

if __name__ == "__main__":
    client.startListening()
