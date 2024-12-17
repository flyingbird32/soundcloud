import json
import os
from utils.logger import log
from utils.tools import obfuscate_auth

class SessionManager:
    def __init__(self, session_file, client):
        self.session_file = session_file
        self.sessions = self._load_sessions()

        if self.sessions == None:
            log(f"failed to load sessions, please make sure sessions.json exists and is set up properly", "error")
            return
        
        log("validating sessions, please wait")

        sessions_to_remove = []

        for session in self.sessions:
            auth_token = session['auth_token']
            response = client.change_username("cat", auth_token)
            if "Permalink change is not allowed" in response.text:
                log(f"removing session: {obfuscate_auth(auth_token)} from list -> username can't be changed at this moment", "error")
                sessions_to_remove.append(session)
            elif response.status_code == 401:
                log(f"removing session: {obfuscate_auth(auth_token)} from list -> invalid token", "error")
                sessions_to_remove.append(session)

        for session in sessions_to_remove:
            self.sessions.remove(session)

        log(f"loaded {len(self.sessions)} sessions")
            
    def _load_sessions(self):
        if not os.path.exists(self.session_file):
            return None

        if os.path.getsize(self.session_file) == 0:
            return None

        try:
            with open(self.session_file, 'r') as file:
                return json.load(file)
        except json.JSONDecodeError as e:
            return None

    def get_sessions(self):
        return self.sessions