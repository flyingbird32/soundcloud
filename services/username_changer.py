from threading import Thread, Lock
import itertools
import time

class UsernameChanger:
    def __init__(self, session_manager, username_manager, client, config):
        self.session_manager = session_manager
        self.username_manager = username_manager
        self.client = client
        self.sessions = self.session_manager.get_sessions()
        self.usernames = itertools.cycle(self.username_manager.get_usernames())
        self.stop_flag = False
        self.session_lock = Lock()

        self.thread_count_per_session = config.get("threads", 10)
        self.rate_limit_sleep_time = config.get("sleep_time_on_rate_limit", 60)

    def _process_username(self, session, session_id, username):
        client_id = session['client_id']
        auth_token = session['auth_token']

        response = self.client.change_username(username, client_id, auth_token)

        if response.status_code == 200:
            print(f"username '{username}' has been claimed on client_id: {client_id}, auth_token: {auth_token}")
            self.stop_flag = True
        elif response.status_code == 401:
            print(f"session {session_id} is invalid (401) and will be removed")
            with self.session_lock:
                self.sessions = [s for s in self.sessions if s != session]
        elif response.status_code == 429:
            print(f"session {session_id} hit rate limit (429) -> waiting for {self.rate_limit_sleep_time} seconds")
            time.sleep(self.rate_limit_sleep_time)  
        else:
            print(f"session {session_id} -> username: {username}, status: {response.status_code}, response: {response.text}")

    def _process_session(self, session, session_id):
        threads = []
        for username in self.usernames:
            if self.stop_flag:
                break

            thread = Thread(target=self._process_username, args=(session, session_id, username))
            threads.append(thread)
            thread.start()

            if len(threads) >= self.thread_count_per_session:
                for thread in threads:
                    thread.join()
                threads = []

        for thread in threads:
            thread.join()

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