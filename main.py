import pytmi
import config

# This is a temporary sort of test file

client = pytmi.TwitchClient(**config.config)

@client.event
async def on_message(message):
    print("Received message")

client.run()
