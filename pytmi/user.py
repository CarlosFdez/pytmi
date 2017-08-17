import enum

class UserType(enum.Enum):
    "Represents a user type of a user in chat"

    EMPTY = "empty"
    MOD = "mod"
    GLOBAL_MOD = "global_mod"
    ADMIN = "admin"
    STAFF = "staff"

class User:
    """Represents a user in the TMI.

    It is available during certain events, such as when a message arrives in a chat channel.
    """

    def __init__(self, color: str, displayName : str, mod : bool, subscriber : bool, turbo : bool, userType : UserType):
        self.color = color
        self.displayName = displayName
        self.mod = mod
        self.subscriber = subscriber
        self.turbo = turbo
        self.userType = userType
