from selenium import webdriver
from selenium.webdriver.firefox.options import Options

import os

day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]

def get_rooms():
	rooms = driver.find_elements_by_css_selector('a[href*="/space/"] span.fc-cell-text')
	print('Rooms available: ')
	for room in rooms:
		room_info = room.text.replace(')', ' ').replace('(', ' ').split(' ')
		# 1 -- number
		# 3 -- capacity

		print(room.text.split(' ')[1])

def get_day_of_week():
	day = driver.find_element_by_class_name('fc-header-toolbar').text.split(',')[0]
	return day_of_week.index(day)

def get_date():
	return driver.find_element_by_class_name('fc-header-toolbar').text.split(',')[1].lstrip()

def set_day(to):
	day = get_day_of_week()
	clicks = to - day
	for _ in range(clicks):
		driver.find_element_by_class_name('fc-next-button').click()

	print("Reserving a room for", day_of_week[get_day_of_week()], get_date())


def rooms_available():
	rooms = get_elements_by_css_selector('div.fc-rows:nth-child(2) table tbody tr')
	for room in rooms:
		# tr td div div
			#  a.s-lc-eq-checkout -- unavailable room
			#  a.s-lc-eq-avail -- available room
				# a.title split by space, 0 returns the time and am/pm
		print('')


# -------------------
print('Starting bot')

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, service_log_path=os.devnull)
driver.get('https://libcal.uccs.edu/reserve/groupstudy')
print('Navigating to libcal.uccs.edu')

set_day(day_of_week.index('Friday'))