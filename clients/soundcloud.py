import requests
import random
from utils.logger import log

class SoundCloud:
    def __init__(self, proxies_file="proxies.txt", max_retries=3):
        self.proxies_file = proxies_file
        self.max_retries = max_retries
        self.proxies = self._load_proxies()

    def _load_proxies(self):
        try:
            with open(self.proxies_file, "r") as file:
                proxies = [line.strip() for line in file if line.strip()]
            if not proxies:
                log("proxy file is empty", "warning")
            return proxies
        except Exception as e:
            log(f"failed to load proxies {e}", "error")
            self.not_using_proxies = True

    def _get_random_proxy(self):
        proxy = random.choice(self.proxies)
        return {
            "http": proxy,
            "https": proxy,
        }

    def _make_request(self, method, url, headers=None, data=None):
        if not self.proxies:
            if method == "GET":
                response = requests.get(url, headers=headers)
            elif method == "PUT":
                response = requests.put(url, headers=headers, data=data)
            return response

        retries = 0
        while retries < self.max_retries:
            proxy = self._get_random_proxy()
            try:
                if method == "GET":
                    response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
                elif method == "PUT":
                    response = requests.put(url, headers=headers, data=data, proxies=proxy, timeout=10)
                return response

            except (requests.RequestException, requests.Timeout) as e:
                retries += 1

    def change_username(self, username, client_id, auth_token):
        url = f"https://api-v2.soundcloud.com/me?client_id={client_id}&app_version=1734100093&app_locale=en"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.7",
            "Authorization": f"OAuth {auth_token}",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://soundcloud.com",
            "Referer": "https://soundcloud.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        data = '{"city":null,"country_code":null,"first_name":"","last_name":"","description":null,"permalink":"asdfhsdfjsfdgjfdhgk657","username":"32"}'
        data = data.replace("asdfhsdfjsfdgjfdhgk657", username)  

        return self._make_request("PUT", url, headers=headers, data=data)

    def check_username(self, username, client_id, auth_token):
        url = f"https://api-v2.soundcloud.com/resolve?url=https%3A//soundcloud.com/{username}&client_id={client_id}&app_version=1734100093&app_locale=en"
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "en-US,en;q=0.7",
            "Authorization": f"OAuth {auth_token}",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Origin": "https://soundcloud.com",
            "Referer": "https://soundcloud.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

        return self._make_request("GET", url, headers=headers)