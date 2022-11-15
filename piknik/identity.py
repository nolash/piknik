import hashlib

class Identity:
    
    def __init__(self, fingerprint):
        self.fp = bytes.fromhex(fingerprint)
        
       
    def uri(self):
        h = hashlib.sha256()
        h.update(self.fp)
        z = h.digest()
        return 'sha256:' + z.hex()

