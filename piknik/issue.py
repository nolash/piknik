import uuid
import json


class Issue:

    def __init__(self, title, issue_id=None):
        if issue_id == None:
            issue_id = str(uuid.uuid4())
        self.id = issue_id
        self.title = title


    @staticmethod
    def from_str(s):
        r = json.loads(s)
        o = Issue(title=r['title'], issue_id=r['id'])
        return o


    def __str__(self):
        return json.dumps({
            'id': str(self.id),
            'title': self.title,
            })


    def __eq__(self, o):
        if o.id != self.id:
            return False
        if o.title != self.title:
            return False
        return True
