import asyncio

from .connection import TMIConnection

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


class TwitchClient:
    def __init__(self, username=None, password=None, channels=[]):
        self.username = username
        self.password = password
        self.channels = channels

        self._connection = TMIConnection(self)

        # A dict of mapped events (name -> listofcallbacks)
        self._events = {}

    ######################################################################
    # SENDING FUNCTIONS
    ####################################################################

    async def send_raw(self, message):
        """Send a raw message. The messages supported are those in the tmi protocol.
        You almost never want to use this. If you want to send a chat message, use send()."""
        await self._connection.send_raw(message)

    async def send_message(self, channel, message):
        "Sends a message to a channel"
        await self._connection.send_message(channel, message)

    async def join(self, channel):
        "Joins a twitch channel."
        await self._connection.join(channel)

    async def part(self, channel):
        "Leaves a twitch channel"
        await self._connection.part(channel)

    ######################################################################
    # EVENTS
    ######################################################################

    def event(self, event_coro):
        "A decorator that registers an event. The object must be a coroutine"
        name = event_coro.__name__
        if name not in self._events:
            self._events[name] = []

        self._events[name].append(event_coro)

    async def send_event(self, event_name : str, *args, **kwargs):
        "Triggers an event and passes arguments to it."
        print("TRIGGERED {}".format(event_name))
        event_name = "on_" + event_name
        for callback in self._events.get(event_name, []):
            asyncio.ensure_future(callback(*args, **kwargs))

    #######################################################################
    # PLUMBING
    ######################################################################

    async def _run(self):
        "Internal method to perform the main loop"
        await self._connection.connect()
        await self._connection.login(self.username, self.password)

        for channel in self.channels:
            await self.join(channel)

        await self._connection.run()

    async def _handle_raw_message(self, message):
        "Internal method to attempt to parse an incoming raw command"
        await self.send_event("raw_message", message)

        print("> " + message)
        await self._message_parser.handle(message)

    def run(self):
        "Starts executing the bot using the provided connection info."
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self._run())
