from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from collections import defaultdict
from datetime import datetime, timedelta

import os
import time

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


def rooms_available(floor):
	room_list = driver.find_elements_by_css_selector('.fc-body tr div div div .fc-rows table tbody tr')
	rooms = defaultdict(list)
	for room in room_list:
		# tr td div div
			#  a.s-lc-eq-checkout -- unavailable room
			#  a.s-lc-eq-avail -- available room
				# a.title split by space, 0 returns the time and am/pm
		slots = room.find_elements_by_css_selector('td div div a.fc-timeline-event')
		for slot in slots:
			current = slot.get_attribute('title').split(' ')
			# 7:30am Friday, February 28, 2020 - Room 212 - Available
			# current[0] - time
			# current[1] - day of week
			# current[2] - month
			# current[3] - day of month
			# current[4] - year
			# current[7] - room number
			# current[9] - status
			if current[7].startswith(str(floor)) and current[9].lower() == "available":
				rooms[current[7]].append(current[0])

	return rooms

# -------------------
print('Starting bot')

times = ['1:00pm', '3:00pm']
floor = 2 + 1 # second floor is the first floor imo

timespan = datetime.strptime(times[1], '%H:%M%p') - datetime.strptime(times[0], '%H:%M%p')
if timespan > timedelta(hours=4):
	print("You cannot reserve a room over 4 hours")
	exit()

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, service_log_path=os.devnull)
driver.get('https://libcal.uccs.edu/reserve/groupstudy')
print('Navigating to libcal.uccs.edu')

set_day(day_of_week.index('Friday'))

rooms = rooms_available(floor)
for room in rooms:
	print(room, ': ', end = '')
	for i in range(len(rooms[room])):
		print(rooms[room][i], end = ' ')
	print('\n-----')

driver.close()