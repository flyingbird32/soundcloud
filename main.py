import json
from managers.session_manager import SessionManager
from managers.username_manager import UsernameManager
from services.username_service import UsernameService
from clients.soundcloud import SoundCloud

def load_config(config_path):
    default_config = {
        "threads": 60
    }

    try:
        with open(config_path, "r") as config_file:
            return json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"failed to load configuration from {config_path}. using defaults. error: {e}")
        return default_config

if __name__ == "__main__":
    config = load_config("config.json")
    client = SoundCloud()

    session_manager = SessionManager("sessions.json", client)
    username_manager = UsernameManager("usernames.txt")

    changer = UsernameService(session_manager, username_manager, client, config)
    changer.run()