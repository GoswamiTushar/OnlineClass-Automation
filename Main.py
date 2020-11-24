import os
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from pynput.mouse import Button, Controller
from credentials import Credentials
import solve_captcha
import time

current_directory = os.getcwd()
driver = webdriver.Firefox(current_directory + r"/MozillaDriver/")

def open_webpage():

	driver.get(r"https://glauniversity.in:8085")

def enter_credentials():

	uni_roll_box = driver.find_element_by_xpath('//*[@id="exampleEmail"]')
	uni_roll_box.send_keys(Credentials.get_GLA_UserID())

	pass_box = driver.find_element_by_xpath('//*[@id="examplePassword"]')
	pass_box.send_keys(Credentials.get_GLA_Password())
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

	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	timings = soup.find_all('b')
	date = re.findall("([0-3][0-9]).([0-1][0-9]).([0-9]{4})", str(timings[0]))
	
	if os.path.exists(current_directory + "/timings.txt"):
		os.remove(current_directory + "/timings.txt")

	fp = open(current_directory + "/timings.txt", 'w')
	fp.write("Schedule for {}/{}/{}\n".format(date[0][0], date[0][1], date[0][2]))
	i = 1

	for time in timings:
		t = re.findall("([0-1][0-9]:[0-5][0-9]) ([AP][M])", str(time))
		x, y, w, z = t[0][0], t[0][1], t[1][0], t[1][1]
		fp.write("{}) From {} {} to {} {}\n".format(i, x, y, w, z))
		i += 1

	fp.close()

def connect_to_zoom():
	try:
		for i in range(1, 20):
			try:
				xpath = "/html/body/div[1]/div[3]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[{}]/div/div/div[2]/a".format(i)
				active_class = driver.find_element_by_xpath(xpath)
				active_class.click()
				if active_class:
					driver.close()
					driver.switch_to.window(driver.window_handles[0])
					break
			except:
				continue
	except:
		pass

	finally:
		time.sleep(3)
		launch_meeting_button = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div')
		launch_meeting_button.click()
		time.sleep(2)
		mouse = Controller()
		mouse.position = (830, 349)
		mouse.click(Button.left, 1)

if __name__ == '__main__':

	# driver = webdriver.Chrome(r"/home/froggy/Programs/Python/OnlineClass-Automation/ChromeDriver/chromedriver")
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
		connect_to_zoom()

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
		connect_to_zoom()
