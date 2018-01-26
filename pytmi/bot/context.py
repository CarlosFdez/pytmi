from pytmi import Message, User

class Context:
    """Defines an object containing information about a bot command invocation.

    """

    def __init__(self, bot, message: Message):
        self.bot = bot
        self.message = message

    @property
    def channel(self):
        """The channel the command was invoced from"""
        return self.message.channel

    @property
    def author(self) :
        """The author that invoked this command"""
        return self.message.author

    async def reply(self, message_content: str):
        "A coroutine used to reply in the channel the command was invoked from"
        await self.bot.send_message(self.channel, message_content)
        