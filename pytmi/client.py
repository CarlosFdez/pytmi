import asyncio

from .connection import TMIConnection

class TwitchClient:
    """Represents a connection to Twitch's Messaging Interface.
    This class is used to join twitch channels and communicate with users.
    """

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

    async def send_raw(self, raw_message : str):
        """Sends a raw command message. The messages supported are those in the tmi protocol.
        You almost never want to use this. 
        If you want to send a chat message, use send_message() instead."""
        await self._connection.send_raw(raw_message)

    async def send_message(self, channel : str, message : str):
        "Send a chat message to a channel"
        await self._connection.send_message(channel, message)

    async def join(self, channel : str):
        "Joins a twitch channel."
        await self._connection.join(channel)

    async def part(self, channel : str):
        "Leaves a twitch channel"
        await self._connection.part(channel)

    ######################################################################
    # EVENTS
    ######################################################################

    def event(self, event_coro):
        "A decorator that registers an event. The registered function must be a coroutine"
        name = event_coro.__name__
        if name not in self._events:
            self._events[name] = []

        self._events[name].append(event_coro)

    async def send_event(self, event_name : str, *args, **kwargs):
        "Triggers an event and passes arguments to it."
        print("TRIGGERED {}".format(event_name))
        event_name = "on_" + event_name

        # If an event exists in this object, call it
        event_fn = getattr(self, event_name, None)
        if event_fn:
            coro = event_fn(*args, **kwargs)
            asyncio.ensure_future(coro)

        # If event has been registered in the collection, call it
        for callback in self._events.get(event_name, []):
            coro = callback(*args, **kwargs)
            asyncio.ensure_future(coro)


    #######################################################################
    # PLUMBING
    ######################################################################

    async def run(self):
        """A coroutine that logs in to twitch, autojoins channels, and begins listening for messages.
        
        Since this is a coroutine, it must run in another coroutine or be registered in the event loop.
        If you want a simpler version, use run_sync()
        """
        await self._connection.connect()
        await self._connection.login(self.username, self.password)

        for channel in self.channels:
            await self.join(channel)

        await self._connection.run()

    def run_sync(self):
        """A blocking function that starts executing the bot using the provided connection info.
        
        This function is equivalent to registered run() on the event loop, and pausing execution
        until the code is complete. Therefore, this function must be performed at the end.
        """
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.run())
