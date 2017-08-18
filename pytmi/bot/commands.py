class Command:
    def __init__(self, name, callback_coro):
        self.name = name
        self.callback_coro = callback_coro

    async def invoke(self, ctx, parser):
        await self.callback_coro(ctx)
        