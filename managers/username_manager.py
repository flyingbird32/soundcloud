class UsernameManager:
    def __init__(self, username_file):
        self.username_file = username_file
        self.usernames = self._load_usernames()

    def _load_usernames(self):
        try:
            with open(self.username_file, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print(f"{self.username_file} not found")
            return []

    def get_usernames(self):
        return self.usernames