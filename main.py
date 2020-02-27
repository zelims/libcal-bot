from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from collections import defaultdict
from datetime import datetime, timedelta

import os
import time

day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]

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


def rooms_available(floor, times):
	room_list = driver.find_elements_by_css_selector('.fc-body tr div div div .fc-rows table tbody tr')
	rooms = defaultdict(list)
	temp_rooms = defaultdict(list)

	for room in room_list:
		slots = room.find_elements_by_css_selector('td div div a.fc-timeline-event')
		for slot in slots:
			current = slot.get_attribute('title').split(' ')
			if (current[7].startswith(str(floor)) or floor == 0) and current[9].lower() == "available":
				if times[0] <= current[0] <= times[1]:
					temp_rooms[current[7]].append(current[0])

	for room in temp_rooms:
		for i in range(len(temp_rooms[room])):
			if times[0] <= temp_rooms[room][i] <= times[1]:
				rooms[room].append(temp_rooms[room][i])

		if rooms[room]:
			if len(rooms[room]) != times[2] or (rooms[room][0] != times[0] or rooms[room][-1] != times[1]):
				try:
					del rooms[room]
				except KeyError:
					continue

	return rooms

# -------------------
print('Starting bot')

# define variables (TODO: Read from file)
times = ['1:00pm', '3:00pm']
floor = -1 + 1

timespan = datetime.strptime(times[1], '%H:%M%p') - datetime.strptime(times[0], '%H:%M%p')
if timespan > timedelta(hours=4):
	print("You cannot reserve a room over 4 hours")
	exit()
if timespan < timedelta(hours=1):
	print('You must reserve at least one hour')
	exit()

times.append((timespan.seconds/3600) * 2 + 1)

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options, service_log_path=os.devnull)
driver.get('https://libcal.uccs.edu/reserve/groupstudy')
print('Navigating to libcal.uccs.edu')

set_day(day_of_week.index('Friday'))

rooms = rooms_available(floor, times)

driver.close()