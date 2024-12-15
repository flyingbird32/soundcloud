import requests

class SoundCloud:
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
        data = data.replace("asdfhsdfjsfdgjfdhgk657", username) # must replace Lol

        response = requests.put(url, headers=headers, data=data)
        return response