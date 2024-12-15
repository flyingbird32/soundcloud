from datetime import datetime
from colorama import Fore, Style, init
from threading import Lock

init(autoreset=True)

log_lock = Lock()

def log(message, log_type="info"):
    log_levels = {
        "error": ("ERROR", Fore.RED),
        "claimed": ("CLAIMED", Fore.GREEN),
        "attempt": ("ATTEMPT", Fore.YELLOW),
        "info": ("INFO", Fore.CYAN),
    }

    log_prefix, color = log_levels.get(log_type.lower(), log_levels["info"])
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"{timestamp} - {color}{log_prefix}{Style.RESET_ALL} - {message}"

    with log_lock:
        print(formatted_message)
