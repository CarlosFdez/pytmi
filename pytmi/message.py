from .user import User

class Message:
    """Represents a user message in the twitch message interface.
    
    Attributes
    -------------
    channel: :class:`str`
        The channel the message was sent from
    content: :class:`str`
        The text content of the message
    author: :class:`User`
        The :class:`User` object that sent this message
    badges: :class:`list`
        TODO: change badges to objects, then document
    bits: :class:`int`
        The number of bits the user sent in this message.
        This value is 0 if no bits were sent.
    """
    
    def __init__(self, channel : str, content : str, author : User, badges, bits : int):
        self.channel = channel
        self.content = content
        self.author = author
        self.badges  = badges
        self.bits = bits
