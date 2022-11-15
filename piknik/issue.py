# standard imports
import uuid
import json
import datetime

# local imports
from piknik.identity import Identity


class Issue:

    def __init__(self, title, issue_id=None):
        if issue_id == None:
            issue_id = str(uuid.uuid4())
        self.id = issue_id
        self.title = title
        self.assigned = []
        self.assigned_time = []
        self.owner_idx = 0


    @staticmethod
    def from_str(s):
        r = json.loads(s)
        o = Issue(title=r['title'], issue_id=r['id'])
        for k in r['assigned'].keys():
            p = Identity(k)
            o.assigned.append(p)
            t = datetime.datetime.utcfromtimestamp(r['assigned'][k])
            o.assigned_time.append(t)
        return o


    def assign(self, identity, t=None):
        if identity in self.assigned:
            raise AlreadyAssignedError(identity)
        if t == None:
            t = datetime.datetime.utcnow()
        self.assigned.append(identity)
        self.assigned_time.append(t)


    def get_assigned(self):
        return list(zip(self.assigned, self.assigned_time))


    def owner(self):
        try:
            return self.assigned[self.owner_idx]
        except Keyerror:
            pass

        raise NoAssignmentsError()


    def set_owner(self, identity):
        r = self.owner()
        if identity == r:
            return False

        for i, v in enumerate(self.assigned):
            if v == identity:
                self.owner_idx = i
                return True

        raise UnknownIdentityError(identity)
        

    def __str__(self):
        o = {
            'id': str(self.id),
            'title': self.title,
            'assigned': {},
            }
        for v in self.get_assigned():
            o['assigned'][v[0].id()] = v[1].timestamp()

        return json.dumps(o)


    def __eq__(self, o):
        if o.id != self.id:
            return False
        if o.title != self.title:
            return False
        return True
