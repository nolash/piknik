import uuid

class Issue:

    def __init__(self, title):
        self.id = uuid.uuid4()
        self.title = title
