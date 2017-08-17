import enum

class UserType(enum.Enum):
    "Represents a user type of a user in chat"

    EMPTY = "empty"
    MOD = "mod"
    GLOBAL_MOD = "global_mod"
    ADMIN = "admin"
    STAFF = "staff"

class User:
    """Contains basic information about a user from a message, usernotice, or userstate."""

    def __init__(self, color, displayName, mod, subscriber, turbo, userType):
        self.color = color
        self.displayName = displayName
        self.mod = mod
        self.subscriber = subscriber
        self.turbo = turbo
        self.userType = userType
