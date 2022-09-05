import os

import nextcord
from nextcord.ext import commands
from boto.s3.connection import S3Connection
from keep_alive import keep_alive

keep_alive()
TOKEN = S3Connection(os.environ['DISCORD_TOKEN'])

class CustomClient(nextcord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

client = CustomClient()

client.run(TOKEN)
