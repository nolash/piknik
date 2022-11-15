# standard imports
import uuid
import json
import datetime

# local imports
from piknik.identity import Identity
from piknik.error import UnknownIdentityError
from piknik.error import AlreadyAssignedError


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
        for i, k in enumerate(r['assigned'].keys()):
            p = Identity(k)
            o.assigned.append(p)
            t = datetime.datetime.utcfromtimestamp(r['assigned'][k])
            o.assigned_time.append(t)
            if r['owner'] == None or k == r['owner']:
                r['owner'] = k
                o.owner_idx = i
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


    def unassign(self, identity):
        for i, v in enumerate(self.assigned):
            if v == identity:
                self.assigned.remove(v)
                if i == self.owner_idx:
                    self.owner_idx = 0
                return True
        raise UnknownIdentityError(identity)


    def owner(self):
        try:
            return self.assigned[self.owner_idx]
        except IndexError:
            pass

        raise UnknownIdentityError


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
            'owner': None,
            }

        for i, v in enumerate(self.get_assigned()):
            aid = v[0].id()
            o['assigned'][aid] = v[1].timestamp()
            if self.owner_idx == i:
                o['owner'] = aid

        return json.dumps(o)


    def __eq__(self, o):
        if o.id != self.id:
            return False
        if o.title != self.title:
            return False
        if len(self.assigned) != len(o.assigned):
            return False
        for i, v in enumerate(self.assigned):
            if o.assigned[i] != v:
                return False
            
        return True
