import json
from managers.session_manager import SessionManager
from managers.username_manager import UsernameManager
from services.username_changer import UsernameChanger
from clients.soundcloud import SoundCloud

def load_config(config_path):

    default_config = {
        "threads": 10,
        "sleep_time_on_rate_limit": 60
    }

    try:
        with open(config_path, "r") as config_file:
            return json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"failed to load configuration from {config_path}. using defaults. error: {e}")
        return default_config

if __name__ == "__main__":
    config = load_config("config.json")

    session_manager = SessionManager("sessions.json")
    username_manager = UsernameManager("usernames.txt")
    client = SoundCloud()

    changer = UsernameChanger(session_manager, username_manager, client, config)
    changer.run()