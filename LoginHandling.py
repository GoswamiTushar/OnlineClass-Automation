import os
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd # for extracting timings and storing them in a csv file 
import credentials
import solve_captcha
import time

def handle_login():

	if os.path.exists(current_directory + r"/captcha.png"):
		os.remove(current_directory + r"/captcha.png")

	driver.get(r"https://glauniversity.in:8085")

	uni_roll_box = driver.find_element_by_xpath('//*[@id="exampleEmail"]')
	uni_roll_box.send_keys(credentials.get_username())

	pass_box = driver.find_element_by_xpath('//*[@id="examplePassword"]')
	pass_box.send_keys(credentials.get_password())
	time.sleep(2)

	captcha_image = driver.find_element_by_xpath('//*[@id="imgCaptcha"]')
	captcha_image.screenshot('captcha.png')
	time.sleep(2)
	captcha_text = solve_captcha.get_text("captcha.png")
	# print(captcha_text)
	captcha_box = driver.find_element_by_xpath('//*[@id="cpatchaTextBox"]')
	captcha_box.send_keys(captcha_text)

def handle_class():
	time.sleep(5)
	online_class_button = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div[4]/div[1]/ul/li[9]/a')
	online_class_button.click()

def get_timings():
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
		handle_login()
		handle_class()
		get_timings()
	except:
		handle_login()
		handle_class()
		get_timings()
