import asyncio

from .connection import TMIConnection

class TwitchClient:
    """Represents a connection to Twitch's Messaging Interface.
    Instances of this class can join twitch channels and communicate with users.
    """

    def __init__(self):
        self._connection = TMIConnection(self)

        # A dict of mapped events (name -> listofcallbacks)
        self._events = {}

    ######################################################################
    # SENDING FUNCTIONS
    ####################################################################

    async def send_raw(self, raw_message : str):
        """This function is a coroutine.

        Internal method to send a raw command message.
        The messages supported are those in the tmi protocol. You almost never want to use this.

        If you want to send a chat message, use :meth:`send_message` instead.
        """
        await self._connection.send_raw(raw_message)

    async def send_message(self, channel : str, message : str):
        """This function is a coroutine.
        
        Send a chat message to a channel
        """
        await self._connection.send_message(channel, message)

    async def join(self, channel : str):
        """This function is a coroutine.
        
        Joins a twitch channel. Twitch channels use the name of the streamer.
        """
        # todo: check if # is required. If it is, append it at the start if DNE.
        await self._connection.join(channel)

    async def part(self, channel : str):
        """This function is a coroutine.
        
        Leaves a twitch channel. Twitch channels use the name of the streamer.
        """
        await self._connection.part(channel)

    ######################################################################
    # EVENTS
    ######################################################################

    def event(self, event_coro):
        """
        A decorator that registers an event. The registered function must be a coroutine.
        
        Example
        -------

        .. code-block:: python

            @client.event
            async def on_message(message):
                print(f"Received message from {message.author}: {message.content}")
        
        """
        name = event_coro.__name__
        if name not in self._events:
            self._events[name] = []

        self._events[name].append(event_coro)

    async def send_event(self, event_name : str, *args, **kwargs):
        """This function is a coroutine.
        
        Internal function that triggers an event and passes arguments to it.
        You almost never want to use this.
        """

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

    async def run(self, username=None, password=None, channels=[]):
        """This function is a coroutine.
        
        Log in to twitch, autojoins the given channels, and begins listening for messages.
        
        Since this is a coroutine, it cannot be run from normal code.
        If you want a simpler version, use :meth:`run_sync` instead.
        """
        await self._connection.connect()
        await self._connection.login(username, password)

        self.username = username

        for channel in channels:
            await self.join(channel)

        await self._connection.run()

    def run_sync(self, username=None, password=None, channels=[]):
        """A blocking function that starts executing the bot using the provided connection info.
        
        This function adds the method :meth:`run` to the event loop, and pauses execution until the client disconnects.
        Therefore, this function must be performed as the last function.
        """
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.run(username, password, channels))
