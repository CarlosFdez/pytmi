from pytmi.bot import TwitchBot
from config import config

bot = TwitchBot(prefix='!')

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello " + ctx.author.name)

bot.run_sync(**config)
