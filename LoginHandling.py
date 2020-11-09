import os
from selenium import webdriver
import pandas as pd # for extracting timings and storing them in a csv file 
import credentials
import solve_captcha
import time

def handle_login():

	current_directory = os.getcwd()

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
	pass


if __name__ == '__main__':
	# driver = webdriver.Chrome(r"/home/froggy/Programs/Python/OnlineClass-Automation/ChromeDriver/chromedriver"))
	driver = webdriver.Firefox()
	handle_login()
	handle_class()
	get_timings()
