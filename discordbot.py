import discord
import os
import webbot

token = os.getenv('DISCORD_TOKEN')
client = discord.Client()

class DiscordBot:
	def __init__(self):
		client.run(token)

	@client.event
	async def on_ready():
		activity = discord.Game(name="type !reserve")
		await client.change_presence(status=discord.Status.online, activity=activity)

	@client.event
	async def on_message(message):
		if message.author == client.user:
			return

		if message.content.startswith('!reserve'):
			params = message.content.split(' ')
			if len(params) == 4:
				if params[3] == "1":
					await message.channel.send("There are no study rooms on the 1st floor!")
				else:
					await message.channel.send("Reserving a room from {} - {} on the {} floor.".format(params[1], params[2], params[3]))
					bot = webbot.WebBot(params[1], params[2], params[3])
			else:
				await message.channel.send("What do you want?!")