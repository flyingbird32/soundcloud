import json
from utils.logger import log

class SessionManager:
    def __init__(self, session_file):
        self.session_file = session_file
        self.sessions = self._load_sessions()
        log(f"loaded {len(self.sessions)} sessions")

    def _load_sessions(self):
        try:
            with open(self.session_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"{self.session_file} not found")
            return []

    def get_sessions(self):
        return self.sessions