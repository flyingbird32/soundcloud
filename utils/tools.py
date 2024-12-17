def obfuscate_auth(auth):
    if len(auth) <= 7:
        return auth 
    return '*' * (len(auth) - 7) + auth[-7:]