import json
from managers.session_manager import SessionManager
from managers.username_manager import UsernameManager
from services.username_service import UsernameService
from clients.soundcloud import SoundCloud
from utils.logger import log

def load_config(config_path):
    try:
        with open(config_path, "r") as config_file:
            return json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return None

def _main():
    config = load_config("config.json")
    if config == None:
        log("failed to load config, please make sure the config is set properly", "error")
        return
    
    client = SoundCloud()
    session_manager = SessionManager("sessions.json", client)
    username_manager = UsernameManager("usernames.txt")

    changer = UsernameService(session_manager, username_manager, client, config)
    changer.run()

if __name__ == "__main__":
    _main()