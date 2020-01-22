from datatype.gender import Gender

class Profile:
    def __init__(self, pid: int, first_name: str, last_name: str, email: str, password: str, gender: Gender):
        self.pid        = pid
        self.first_name = first_name
        self.last_name  = last_name
        self.email      = email
        self.password   = password
        self.gender     = gender
