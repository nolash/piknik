import hashlib


class Identity:
    
    def __init__(self, fingerprint):
        self.__id = bytes.fromhex(fingerprint)
       

    def id(self):
        return self.__id.hex()

       
    def uri(self):
        h = hashlib.sha256()
        h.update(self.id)
        z = h.digest()
        return 'sha256:' + z.hex()
