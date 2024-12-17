from threading import Thread, Lock
import itertools
import time
from utils.logger import log

class UsernameService:
    def __init__(self, session_manager, username_manager, client, config):
        self.session_manager = session_manager
        self.username_manager = username_manager
        self.client = client
        self.sessions = self.session_manager.get_sessions()
        self.usernames = itertools.cycle(self.username_manager.get_usernames())
        self.stop_flag = False
        self.session_lock = Lock()

        self.thread_count_per_session = config.get("threads")

    def _process_username(self, session, session_id, username):
        client_id = session['client_id']
        auth_token = session['auth_token']

        response = self.client.check_username(username, client_id, auth_token)
        if response.status_code == 404:
            response = self.client.change_username(username, client_id, auth_token)
            if response.status_code == 200:
                log(f"[{session_id}] username '{username}' has been claimed on client_id: {client_id}, auth_token: {auth_token}", "claimed")
                self.stop_flag = True
        elif response.status_code == 200:
            log(f"[{session_id}] -> username: {username}", "attempt")
        else:
            log(f"[{session_id}] -> username: {username}; unknown response: {response.status_code}", "INFO")

    def _process_session(self, session, session_id):
        while not self.stop_flag:
            usernames = list(itertools.islice(self.usernames, 20))
            threads = []

            for username in usernames:
                thread = Thread(target=self._process_username, args=(session, session_id, username))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            if self.stop_flag or len(usernames) < 20:
                break

    def run(self):
        while self.sessions:
            threads = []
            with self.session_lock:
                snapshot = list(enumerate(self.sessions))

            for i, session in snapshot:
                thread = Thread(target=self._process_session, args=(session, i + 1))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()