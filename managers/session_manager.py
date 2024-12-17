import json
import os
from utils.logger import log
from clients.soundcloud import SoundCloud

class SessionManager:
    def __init__(self, session_file, client):
        self.session_file = session_file
        self.sessions = self._load_sessions()
        log(f"loaded {len(self.sessions)} sessions")

        sessions_to_remove = []

        for session in self.sessions:
            client_id = session['client_id']
            auth_token = session['auth_token']
            response = client.change_username("cat", client_id, auth_token)
            if "Permalink change is not allowed" in response.text:
                log(f"removing client: {auth_token} from list -> username can't be changed at this moment", "ERROR")
                sessions_to_remove.append(session)
            elif response.status_code == 401:
                log(f"removing client: {auth_token} from list -> invalid token", "ERROR")
                sessions_to_remove.append(session)

        for session in sessions_to_remove:
            self.sessions.remove(session)
            
    def _load_sessions(self):
        if not os.path.exists(self.session_file):
            raise FileNotFoundError(f"session file '{self.session_file}' does not exist")

        if os.path.getsize(self.session_file) == 0:
            raise ValueError(f"session file '{self.session_file}' is empty")

        try:
            with open(self.session_file, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"session file '{self.session_file}' contains invalid JSON; error: {e}")

    def get_sessions(self):
        return self.sessions