from .user import User

class Message:
    """Represents a message in the twitch message interface."""
    
    def __init__(self, channel : str, content : str, author : User, badges, bits : int):
        "The channel the message was sent from"
        self.channel = channel

        self.content = content

        "The user data of the user who sent the message"
        self.author = author

        self.badges  = badges

        "The number of bits in the message, or None if nothing was sent"
        self.bits = bits
