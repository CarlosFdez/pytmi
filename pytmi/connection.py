import asyncio
import re
import ssl

from .user import UserType, User
from .message import Message

def parse_tags(tagstring : str) -> dict:
    """Parse tags. Details at http://ircv3.net/specs/core/message-tags-3.2.html
    This parser is not "complete" and does minimal parsing.
    """
    # as <tag> and <escaped value> cannot contain ;, its ok to split on ;
    result = {}

    tags = tagstring.split(';')
    for tag in tags:
        (key, sep, value_str) = tag.partition('=')
        result[key] = value_str

    return result

def parse_badges(badgestr : str):
    """Parses a badge string in the format of name1/version1,name2/version2.
    version is an integer representing the badge's version
    """
    badges = badgestr.split(',')
    badges = [s.split('/') for s in badges]
    badges = [(x, int(y)) for (x, y) in badges]
    return badges

def parse_user(tags : dict):
    return User(
        color=tags.get("color"),
        id=tags.get("user-id"),
        name=tags.get("display-name"),
        mod=tags.get("mod") == "1",
        subscriber=tags.get("subscriber") == "1",
        turbo=tags.get("turbo") == "1",
        userType=UserType(tags.get("user-type", UserType.EMPTY)))

class RegexHandler:
    "A simple regex -> callback mapper that supports async"
    def __init__(self):
        self.handlers = []

    def add(self, regex_str, handler):
        compiled = re.compile(regex_str)
        self.handlers.append( (compiled, handler) )

    async def handle(self, message):
        for (expr, handler) in self.handlers:
            match = expr.fullmatch(message)
            if match:
                await handler(match, message)
                return

class TMIConnection:
    """Represents the pipeline of the twitch TMI
    
    The dispatcher is any object that supports a send_event(event_name, *args, **kwargs) object
    """
    def __init__(self, dispatcher):        # todo: move to some dedicated parser/bridge
        self._message_parser = RegexHandler()
        self._dispatcher = dispatcher

        self._message_parser.add(
            "^PING (?P<replyto>:[^\s]+)$",
            self._handle_ping)

        self._message_parser.add(
            "^@(?P<tags>\S+) (?P<mask>:\S+) PRIVMSG (?P<channel>\S+) :(?P<message>.*)$",
            self._handle_privmsg)

    async def send_raw(self, message):
        # todo: throttle: twitch has api limits
        self.writer.write((message + "\r\n").encode())
        await self.writer.drain()
        print("< " + message)

    async def send_message(self, channel, message):
        await self.send_raw("PRIVMSG {} :{}".format(channel, message))

    async def join(self, channel):
        await self.send_raw("JOIN {}".format(channel))

    async def part(self, channel):
        "Leaves a twitch channel"
        await self.send_raw("PART {}".format(channel))

    async def connect(self):
        "Internal method to connect to the server. This populates self.reader and self.writer"
        # attempt to connect (todo: separate?)
        sslctx = ssl.create_default_context()
        self.reader, self.writer = await asyncio.open_connection(
            host="irc.chat.twitch.tv",
            port=443,
            ssl=sslctx,
            server_hostname="irc.chat.twitch.tv")

    async def login(self, username, password):
        await self.send_raw("PASS {}".format(password))
        await self.send_raw("NICK {}".format(username))

        # Enable twitch tags to receive additional data about users
        # We don't use membership event data in this bot
        await self.send_raw("CAP REQ :twitch.tv/tags")
        await self.send_raw("CAP REQ :twitch.tv/commands")

    async def run(self):
        _buffer = ""
        while True:
            _buffer += (await self.reader.read(2048)).decode()

            # Split into individual line.
            # If the buffer ends with "\r\n", then the last entry will be "". If not, its an incomplete message.
            # pop() handles both of these use cases
            lines = _buffer.split("\r\n")
            _buffer = lines.pop()

            for line in lines:
                asyncio.ensure_future(self._handle_raw_message(line))

    #######################################################################
    # HANDLERS FOR RAW EVENTS
    #######################################################################

    async def _handle_raw_message(self, raw_message):
        "Internal method to attempt to parse an incoming raw command"
        print("> " + raw_message)
        await self._dispatcher.send_event("raw_message", raw_message)
        await self._message_parser.handle(raw_message)

    async def _handle_ping(self, match, raw_message):
        await self.send_raw("PONG {}".format(match["replyto"]))
        await self._dispatcher.send_event("ping")

    async def _handle_privmsg(self, match, raw_message):
        "Triggered when a message is posted in a channel"

        # todo: do we need to parse the mask? I think the tags contain enough data
        channel = match['channel']
        text = match['message']

        tags = parse_tags(match['tags'])
        badges = parse_badges(tags.get('badges', ''))
        user = parse_user(tags)
        bits = int(tags["bits"]) if "bits" in tags else None

        # NOTE USERNOTICE USERSTATE AND PRIVMSG ARE SIMILAR
        # privmsg has bits
        # usernotice has a lot more
        # userstate is similar

        message = Message(
            channel=channel,
            content=text,
            author=user,
            badges=badges,
            bits=bits
        )
        
        await self._dispatcher.send_event("message", message)
