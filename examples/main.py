import pytmi
from config import config

client = pytmi.TwitchClient(prefix='!', **config.config)

@client.event
async def on_message(message):
    print("Received message")

client.run_sync()
