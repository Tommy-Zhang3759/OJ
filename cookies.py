class Cookies:
    class cookie:
        def __init__(self, ip, name, zid) -> None:
            import time
            self.ip = ip
            self.name = name
            self.cookie = self.sha256(time.ctime() + zid)

        def sha256(message):
            import hashlib
            sha256_hash = hashlib.sha
            sha256_hash.update(message.encode('utf-8'))
            return sha256_hash.hexdigest()

sss = 9