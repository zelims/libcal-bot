from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException

from collections import defaultdict
from datetime import datetime, timedelta

import os
import time
import json

class WebBot:
	day_of_week = ["Monday", "Tuesday", "Wednesday", "Thu=rsday", "Friday", "Saturday", "Sunday" ]

	def get_day_of_week(self):
		day = self.driver.find_element_by_class_name('fc-header-toolbar').text.split(',')[0]
		return self.day_of_week.index(day)

	def get_date(self):
		return self.driver.find_element_by_class_name('fc-header-toolbar').text.split(',')[1].lstrip()

	def set_day(self, to):
		day = self.get_day_of_week()
		clicks = to - day
		for _ in range(clicks):
			self.driver.find_element_by_class_name('fc-next-button').click()


	def rooms_available(self, floor, times):
		room_list = self.driver.find_elements_by_css_selector('.fc-body tr div div div .fc-rows table tbody tr')
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

	def reserve_room(self, number, times): 
		self.driver.find_element_by_xpath("//a[contains(@title, '" + times[0] + "') and contains(@title, '" + number + "')]").click()

		time.sleep(1)

		select = self.driver.find_element_by_xpath("//select[@id='bookingend_1']")
		all_options = select.find_elements_by_tag_name("option")
		for option in all_options:
			if times[1] in option.text:
				option.click()

		self.driver.find_element_by_xpath('//button[@id="submit_times"]').click()

	def login(self, username, password):
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
		self.driver.find_element_by_xpath('//input[@id="username"]').send_keys(username)
		self.driver.find_element_by_xpath('//input[@id="password"]').send_keys(password)
		self.driver.find_element_by_xpath('//button[@id="s-libapps-login-button"]').click()

	def complete_booking(self, first_name, last_name, email, nick):
		WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'terms_accept')))
		# accept terms
		self.driver.find_element_by_xpath('//button[@id="terms_accept"]').click()

		self.driver.find_element_by_xpath('//input[@id="fname"]').send_keys(first_name)
		self.driver.find_element_by_xpath('//input[@id="lname"]').send_keys(last_name)
		self.driver.find_element_by_xpath('//input[@id="email"]').send_keys(email)
		self.driver.find_element_by_xpath('//input[@id="nick"]').send_keys(nick)

		select = Select(self.driver.find_element_by_xpath('//select[@id="q1328"]'))
		select.select_by_index(3)

		self.driver.find_element_by_xpath('//button[@id="s-lc-eq-bform-submit"]').click()

	def create(self, dayofweek, startTime, endTime, floor):
		times = [startTime, endTime]

		with open('config.json') as f:
			config = json.load(f)

		timespan = datetime.strptime(times[1], '%H:%M%p') - datetime.strptime(times[0], '%H:%M%p')
		if timespan > timedelta(hours=4):
			return "You cannot reserve a room over 4 hours"
		if timespan < timedelta(hours=1):
			return 'You must reserve at least one hour'

		times.append((timespan.seconds/3600) * 2 + 1)

		options = Options()
		options.headless = True
		self.driver = webdriver.Firefox(options=options, service_log_path=os.devnull)
		self.driver.get('https://libcal.uccs.edu/reserve/groupstudy')

		self.set_day(self.day_of_week.index(dayofweek.capitalize()))

		rooms = self.rooms_available(floor, times)
		room = next(iter(rooms))

		self.reserve_room(room, times)

		time.sleep(1)
		
		self.login(config["email"].split('@')[0], config["password"])

		time.sleep(1)

		self.complete_booking(config["first_name"], config["last_name"], config["email"], config["initials"])

		time.sleep(1)

		try:
			WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'The following reservations were made')]")))
			output = 'Reserved room {} from {} - {} on {}!'.format(room, startTime, endTime, dayofweek)
		except TimeoutException:
			output = "Some error has occured"

		self.driver.close()
		return output

	def __init__(self):
		pass