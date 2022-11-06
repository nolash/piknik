import uuid
import json


class Issue:

    def __init__(self, title):
        self.id = uuid.uuid4()
        self.title = title


    def __str__(self):
        return json.dumps({
            'id': str(self.id),
            'title': self.title,
            })
