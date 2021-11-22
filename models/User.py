class User:
    def __init__(self, id, username, password, fullname, email, auth_history):
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.email = email
        self.auth_history = auth_history

    def __str__(self):
        return "User(id='%s')" % self.id

    def jsonify(self):
        return {
            "username": self.username,
            "passord": self.password,
            "id": self.id,
            "fullname": self.fullname,
            "email": self.email,
            "auth_history": self.auth_history
        }
