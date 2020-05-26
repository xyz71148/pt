class Identity(object):
    def __init__(self, id, email):
        self.id = id
        self.email = email

    def __str__(self):
        return "Identity(id='%s')" % self.id