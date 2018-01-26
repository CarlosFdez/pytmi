import pytmi

from .parser import StringParser
from .context import Context
from .commands import Command

class TwitchBot(pytmi.TwitchClient):
    """A subclass of TwitchClient used to respond to bot commands.
    """

    def __init__(self, prefix=None):
        super().__init__()
        self.prefix = prefix

        self._all_commands = {}

    def add_command(self, command: Command):
        """Adds a command to the bot. You'll usually use the command decorator instead"""
        if command.name in self._all_commands:
            pass # todo: throw exception

        self._all_commands[command.name] = command

    def command(self, name=None):
        """
        A decorator used to register a function as a command to the bot.
        The name of the command is set with either the name argument, or the name of the given function

        Example
        -------

        Creates a bot, with a !hello command

        .. code-block:: python

            bot = TwitchBot(prefix='!')

            @bot.command()
            async def hello(ctx):
                await ctx.reply("Hello " + ctx.author.name)
        """
        def decorator(fn_coro):
            cmd_name = name or fn_coro.__name__
            cmd = Command(name=cmd_name, callback_coro=fn_coro)
            self.add_command(cmd)
            return fn_coro
        return decorator

    async def on_message(self, message : pytmi.Message):
        "Internal async event which calls process_message."
        await self.process_message(message)

    async def process_message(self, message : pytmi.Message):
        """This function is a coroutine.
        
        Internal method that examines the message object for commands.
        """

        # todo: ensure the message isn't from the bot
        parser = StringParser(message.content)
        if not parser.skip_value(self.prefix):
            return

        command_name = parser.consume_word()
        if not command_name in self._all_commands:
            return

        command = self._all_commands[command_name]
        ctx = Context(self, message)
        await command.invoke(ctx, parser)
