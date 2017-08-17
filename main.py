import pytmi
import config

# This is a temporary test file, will go away in future version 

client = pytmi.TwitchClient(**config.config)

@client.event
async def on_message(message):
    print("Received message")

client.run_sync()
