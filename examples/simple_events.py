import pytmi
from config import config

client = pytmi.TwitchClient()

@client.event
async def on_message(message):
    print(f"Received message from {message.author}: {message.content}")

client.run_sync(**config)
