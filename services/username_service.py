from threading import Thread, Lock, Semaphore
import itertools
import time
from utils.logger import log
from utils.tools import obfuscate_auth

class UsernameService:
    def __init__(self, session_manager, username_manager, client, config, webhook):
        self.session_manager = session_manager
        self.username_manager = username_manager
        self.client = client
        self.webhook = webhook

        self.checks_per_session = config.get("checks_per_session")
        self.cooldown_after_ratelimit = config.get("cooldown_after_ratelimit")
        self.should_print_attempts = config.get("log_attempts")
        self.thread_limit = Semaphore(config.get("threads"))  

        self.sessions = self.session_manager.get_sessions()
        self.usernames = itertools.cycle(self.username_manager.get_usernames())

        self.stop_flag = False
        self.session_lock = Lock()
        self.stop_lock = Lock()

    def _process_username(self, session, session_id, username):
        if self.stop_flag:
            return

        auth_token = session['auth_token']
        response = self.client.check_username(username, auth_token)
        
        if response.status_code == 404:
            start_time = time.perf_counter()
            response = self.client.change_username(username, auth_token)
            end_time = time.perf_counter()
            elapsed_time_ms = (end_time - start_time) * 1000

            if response.status_code == 200:
                with self.stop_lock:
                    if not self.stop_flag: 
                        parsed = f"{elapsed_time_ms:.2f}"
                        log(f"[{session_id}] username '{username}' has been claimed on auth_token: {obfuscate_auth(auth_token)} in {parsed}ms", "claimed")
                        self.webhook.send_webhook(username, auth_token, parsed)
                        self.stop_flag = True
        elif response.status_code == 200:
            if self.should_print_attempts and not self.stop_flag:
                log(f"[{session_id}] -> username: {username}", "attempt")
        elif response.status_code == 429:
            log(f"currently rate limited, trying again in: {self.cooldown_after_ratelimit} seconds", "error")
            time.sleep(self.cooldown_after_ratelimit)
        else:
            log(f"[{session_id}] -> username: {username}; unknown response: {response.status_code}", "info")

    def _process_session(self, session, session_id):
        while not self.stop_flag:
            usernames = list(itertools.islice(self.usernames, self.checks_per_session))
            threads = []

            for username in usernames:
                if self.stop_flag:
                    break

                self.thread_limit.acquire()  
                thread = Thread(target=self._thread_wrapper, args=(session, session_id, username))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            if self.stop_flag or len(usernames) < self.checks_per_session:
                break

    def _thread_wrapper(self, session, session_id, username):
        try:
            self._process_username(session, session_id, username)
        finally:
            self.thread_limit.release() 

    def run(self):
        session_threads = []

        for i, session in enumerate(self.sessions):
            if self.stop_flag:
                break

            thread = Thread(target=self._process_session, args=(session, i + 1))
            session_threads.append(thread)
            thread.start()

        for thread in session_threads:
            thread.join()