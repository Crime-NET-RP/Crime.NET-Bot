import nextcord, os
from dotenv import load_dotenv
from nextcord.ext import commands
from flask import Flask
from boto.s3.connection import S3Connection
from threading import Thread

load_dotenv()

app = Flask('')
@app.route('/')
def home():
	return 'Running!'
def run():
	app.run(port=int(os.environ.get('PORT', 33507)))
def keep_alive():
	Thread(target=run).start()

version = 'Command Test'
TOKEN = os.environ['DISCORD_TOKEN']
description = 'Crime.NET Bot'
intents = nextcord.Intents.default()

client = commands.Bot(command_prefix='/', description=description, intents=intents)

def embed(title, description, reason) -> nextcord.Embed:
	return nextcord.Embed(
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

@client.slash_command(name='ping', description='Returns bot latency')
async def ping(ctx):
	await ctx.message.respond(f'Pong! {client.latency * 100} ms')
	await ctx.send(embed=embed(':ping_pong: Pong!', f'{client.latency * 100} ms', f'{ctx.user} used the "ping" command'))

@client.slash_command(name='message', description='Sends a message to a user', dm_permission=False, default_member_permissions=commands.Permissions(administrator=True))
async def message(ctx, user, message: str):
	try:
		await user.send(embed=embed(f'Message from {ctx.user}:', f'{message}', f'an admin of {ctx.guild} used the "message" command'))
	except Exception:
		await ctx.respond('Could not send message!')
	else:
		await ctx.respond(f'Message sent to {user}!')

if __name__ == '__main__':
	keep_alive()
	client.run(TOKEN)
