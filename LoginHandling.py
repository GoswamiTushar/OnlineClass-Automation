import os
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd # for extracting timings and storing them in a csv file 
import credentials
import solve_captcha
import time

def open_webpage():

	driver.get(r"https://glauniversity.in:8085")

def enter_credentials():

	uni_roll_box = driver.find_element_by_xpath('//*[@id="exampleEmail"]')
	uni_roll_box.send_keys(credentials.get_username())

	pass_box = driver.find_element_by_xpath('//*[@id="examplePassword"]')
	pass_box.send_keys(credentials.get_password())
	time.sleep(2)


def handle_login():

	if os.path.exists(current_directory + r"/captcha.png"):
		os.remove(current_directory + r"/captcha.png")

	captcha_image = driver.find_element_by_xpath('//*[@id="imgCaptcha"]')
	captcha_image.screenshot('captcha.png')
	time.sleep(2)
	captcha_text = solve_captcha.get_text("captcha.png")
	# print(captcha_text)
	captcha_box = driver.find_element_by_xpath('//*[@id="cpatchaTextBox"]')
	captcha_box.send_keys(captcha_text)
	time.sleep(5)

	try:
		ok_button = driver.find_element_by_xpath('/html/body/div[5]/div/div[3]/div/button')
		if ok_button:
			ok_button.click()
			time.sleep(2)
			handle_login()
	except:
		pass


def handle_class():
	time.sleep(5)
	try:
		online_class_button = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div[4]/div[1]/ul/li[9]/a')
		online_class_button.click()
	except:
		# handle_login()
		pass
		exit()

def get_timings():

	calender = driver.find_element_by_xpath('//*[@id="LecDate"]')
	calender.click()
	# 10thDate = driver.find_element_by_xpath('/html/body/div[4]/div[1]/table/tbody/tr[3]/td[3]')
	# 10thDate.click()

	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser').prettify()
	if os.path.exists(current_directory + "/schedule_page.html"):
		os.remove(current_directory + "/schedule_page.html")

	fp = open(current_directory + "/schedule_page.html", 'w')
	fp.write(soup)
	fp.close()

if __name__ == '__main__':

	# driver = webdriver.Chrome(r"/home/froggy/Programs/Python/OnlineClass-Automation/ChromeDriver/chromedriver"))
	driver = webdriver.Firefox()
	current_directory = os.getcwd()
	try:
		open_webpage()
		time.sleep(5)
		enter_credentials()
		time.sleep(5)
		handle_login()
		time.sleep(5)
		handle_class()
		time.sleep(5)
		get_timings()
	except:
		open_webpage()
		time.sleep(5)
		enter_credentials()
		time.sleep(5)
		handle_login()
		time.sleep(5)
		handle_class()
		time.sleep(5)
		get_timings()
