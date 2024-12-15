from managers.session_manager import SessionManager
from managers.username_manager import UsernameManager
from clients.soundcloud import SoundCloud
from services.username_changer import UsernameChanger

if __name__ == "__main__":
    session_manager = SessionManager("sessions.json")
    username_manager = UsernameManager("usernames.txt")
    
    client = SoundCloud()

    changer = UsernameChanger(session_manager, username_manager, client)
    changer.run()