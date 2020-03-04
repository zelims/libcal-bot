import discord
import os
import webbot
import json

client = discord.Client()

class DiscordBot:
	def __init__(self):
		with open('config.json') as f:
			config = json.load(f)
		client.run(config["token"])

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
			if len(params) == 5:
				if params[3] == "1":
					await message.channel.send("There are no study rooms on the 1st floor!")
				else:
					await message.channel.send("Reserving a room... please wait!")
					bot = webbot.WebBot()
					await message.channel.send(bot.create(params[1], params[2], params[3], params[4]))
			else:
				await message.channel.send("!reserve [day of week] [start time] [end time] [floor]")