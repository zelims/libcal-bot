from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import os


def get_rooms():
	rooms = driver.find_elements_by_css_selector('a[href*="/space/"] span.fc-cell-text')
	print('Rooms available: ')
	for room in rooms:
		room_info = room.text.replace(')', ' ').replace('(', ' ').split(' ')
		# 1 -- number
		# 3 -- capacity

		print(room.text.split(' ')[1])


print('Starting bot')

options = Options()
# options.headless = True
#, service_log_path=os.devnull
driver = webdriver.Firefox(options=options)
driver.get('https://libcal.uccs.edu/reserve/groupstudy')
print('Navigating to libcal.uccs.edu')

get_rooms()