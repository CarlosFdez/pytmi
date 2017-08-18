# PyTMI

A python library for communicating in the Twitch Messaging Interface ([docs](https://dev.twitch.tv/docs/v5/guides/irc/))

## Why a new library
Unfortunately, I haven't found a good python library for twitch that was simple, extendable, and scalable. While good libraries exist for Javascript ([tmi.js](https://github.com/tmijs/tmi.js)), and there have been many great advancements in Javascript, I much prefer Python in the backend. Python is much easier to learn to use effectively, which makes it easier for my brother to make tweaks to bots on his own.

While Python IRC libraries exist (TMI is a weird IRC), most are too complicated to use, not extendable, don't support asyncio, or are for python 2.

Many of the ideas used in this library came from [discord.py](https://github.com/Rapptz/discord.py), a library for creating bots for discord.

## Example

This is an example of the core functionality.

```py
import pytmi

config = {
    'username': "botname",
    'password': "oauthstring",
    'channels': ["#channelname"]
}

client = pytmi.TwitchClient(**config)

@client.event
async def on_message(message):
    print("Received message")

client.run_sync()
```

This is an example of the bot command functionality.

```py
from pytmi.bot import TwitchBot

config = {
    'username': "botname",
    'password': "oauthstring",
    'channels': ["#channelname"]
}

client = pytmi.TwitchClient(prefix='!', **config)

@bot.command()
async def hello(ctx):
    await ctx.reply("Hello " + ctx.author.name)

client.run_sync()
```

More examples are available in the examples/ folder.
