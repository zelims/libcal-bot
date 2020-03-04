import discordbot
import json
import re

email_regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

print('[*] Starting bot')
print('[*] Parsing config')
with open('config.json') as f:
	config = json.load(f)

if len(config) != 6:
	print('[!] Config is missing a field!')
	exit()

for entry in config:
	if config[entry] == "":
		print('[!] Config entry "{}" is empty!'.format(entry))
		exit()

if not re.search(email_regex, config["email"]):
	print('[!] Email format in config is incorrect!')
	exit()

if len(config["initials"]) != 2:
	print('[!] Initials format in config is incorrect!')
	exit()

bot = discordbot.DiscordBot(config)