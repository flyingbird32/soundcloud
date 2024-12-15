from threading import Thread
import itertools
import time

class UsernameChanger:
    def __init__(self, session_manager, username_manager, client):
        self.session_manager = session_manager
        self.username_manager = username_manager
        self.client = client
        self.sessions = self.session_manager.get_sessions()
        self.usernames = itertools.cycle(self.username_manager.get_usernames())  

    def _process_session(self, session, session_id):
        client_id = session['client_id']
        auth_token = session['auth_token']
        
        for username in self.usernames:  
            response = self.client.change_username(username, client_id, auth_token)
            print(f"session {session_id} -> username: {username}, status: {response.status_code}, response: {response.text}")
            
            time.sleep(1)  

    def run(self):
        threads = []
        for i, session in enumerate(self.sessions):
            thread = Thread(target=self._process_session, args=(session, i + 1))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
