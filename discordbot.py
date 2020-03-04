import discord
import os
import webbot

client = discord.Client()
config = {}

class DiscordBot:
	def __init__(self, config):
		client.run(config["token"])

	@client.event
	async def on_ready():
		activity = discord.Game(name="type !reserve")
		await client.change_presence(status=discord.Status.online, activity=activity)
		print('[*] Waiting for commands')

	@client.event
	async def on_message(message):
		if message.author == client.user:
			return

		if message.content.startswith('!reserve'):
			params = message.content.split(' ')
			if len(params) == 5:
				if params[4] == "1":
					await message.channel.send("There are no study rooms on the 1st floor!")
				else:
					await message.channel.send("Reserving a room... please wait!")
					bot = webbot.WebBot(config)
					await message.channel.send(bot.create(params[1], params[2], params[3], params[4]))
			else:
				await message.channel.send("!reserve [day of week] [start time] [end time] [floor]")