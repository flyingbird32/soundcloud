import json
import os
from utils.logger import log

class SessionManager:
    def __init__(self, session_file):
        self.session_file = session_file
        self.sessions = self._load_sessions()
        log(f"loaded {len(self.sessions)} sessions")

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