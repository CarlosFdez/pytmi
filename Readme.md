# PyTMI

A python library for communicating in the Twitch Messaging Interface ([docs](https://dev.twitch.tv/docs/v5/guides/irc/))

## Why a new library
Unfortunately, I haven't found a good python library for twitch that was simple, extendable, and scalable. Good libraries exist for Javascript ([tmi.js](https://github.com/tmijs/tmi.js)), but I haven't found something for Python.

While Python IRC libraries exist (twitch message interface is a weird IRC), most are too complicated to use, not extendable, don't support asyncio, or are for python 2.

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
