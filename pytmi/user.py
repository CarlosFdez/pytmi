import enum

class UserType(enum.Enum):
    "Represents a user type of a user in chat"

    EMPTY = "empty"
    MOD = "mod"
    GLOBAL_MOD = "global_mod"
    ADMIN = "admin"
    STAFF = "staff"

class User:
    """Represents a twitch user in a channel.

    It is available during certain events, such as when a message arrives in a chat channel.

    Note that this is not fully parsed, and much of the data is still raw.
    This is highly subject to change in future versions of this library.

    Attributes
    -------------
    color: :class:`str`
        The color code as a hexadecimal string (ex: #0D4200)
    id: :class:`str`
        The id of the twitch user as a raw string.
    name: :class:`str`
        The display name of the user
    mod: :class:`bool`
        `True` if this user is a moderator. `False` otherwise.
        It is usually better to check the badges on the
        :class:`Message` when checking for permissions.
    subscriber: :class:`bool`
        `True` if this user is a subscriber. `False` otherwise.
    turbo: :class:`bool`
        `True` if this user has a turbo badge. `False` otherwise.
    userType: :class:`UserType`
        The type of user this object represents.
        
    """

    def __init__(self, color: str, id: str, name : str, mod : bool, subscriber : bool, turbo : bool, userType : UserType):
        self.color = color
        self.id = id
        self.name = name
        self.mod = mod
        self.subscriber = subscriber
        self.turbo = turbo
        self.userType = userType
