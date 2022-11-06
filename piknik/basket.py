

class Basket:
    
    def __init__(self):
        self.issues = {
                'default': [],
                }
        self.issues_rev = {}


    def add(self, issue):
        self.issues['default'].append(issue)
        self.issues_rev[issue.id] = issue


    def get(self, issue_id):
        return self.issues_rev[issue_id]
