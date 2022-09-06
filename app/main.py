import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands
from boto.s3.connection import S3Connection
from keep_alive import keep_alive

load_dotenv()
keep_alive()

version = 'v-Unreleased'
TOKEN = os.environ['DISCORD_TOKEN']
description = ''
intents = nextcord.Intents.default()

client = commands.Bot(command_prefix='/', description=description, intents=intents)

def embed(title, description, reason):
	nextcord.Embed(
		title=title,
		description=description,
		color=0x360404
	).set_author(
		name=f"Crime.NET Bot {version}",
		icon_url="https://cdn.discordapp.com/icons/1001291176252543129/a_16d95fd874430473a19bd2506d91af10.gif?size=160"
	).set_footer(
		text=f"This message was sent because {reason}."
	)

@client.event
async def on_ready():
	print(f'Logged in as {client.user} (ID: {client.user.id})')
	await client.change_presence(activity=nextcord.Game(name=f'{version}'))

@client.command()
async def ping(ctx):
    await ctx.send(embed(':ping_pong: Pong!', '{0}'.format(round(client.latency, 1)), 'the `ping` command was used'))

client.run(TOKEN)
