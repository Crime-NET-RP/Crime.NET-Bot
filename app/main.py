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
	return "I'm alive"
def run():
	app.run(debug=True, port=int(os.environ.get('PORT', 33507)))
def keep_alive():
	Thread(target=run).start()

version = 'First Release'
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

@client.slash_command(name='ping', description='Returns bot latency')
async def ping(ctx, interaction):
	if interaction.type == nextcord.InteractionType.application_command:
		await client.process_application_commands(interaction)
		await interaction.response.send_message(embed(':ping_pong: Pong!', f'{round(client.latency, 1)} ms', 'the `ping` command was used'))

if __name__ == '__main__':
	keep_alive()
	client.run(TOKEN)
