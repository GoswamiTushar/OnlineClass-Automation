import os
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from pynput.mouse import Button, Controller
from credentials import Credentials
import solve_captcha
import time
"""Main.py is modularised into different functions which handles different sections 
of of page required for automation"""
current_directory = os.getcwd()
driver = webdriver.Firefox(current_directory + r"/MozillaDriver/") 

def open_webpage():
    """This function opens GLA's student portal"""
    driver.get(r"https://glauniversity.in:8085")

def enter_credentials():
    """This function handles sending credentials to uni roll and password box on portal's login page."""
    uni_roll_box = driver.find_element_by_xpath('//*[@id="exampleEmail"]')
    uni_roll_box.send_keys(Credentials.get_GLA_UserID())

    pass_box = driver.find_element_by_xpath('//*[@id="examplePassword"]')
    pass_box.send_keys(Credentials.get_GLA_Password())
    time.sleep(2)


def handle_captcha():
    """This function takes screenshot of captcha image, activated solve_captcha.py module and enters the solved captcha string in captcha box
    If the captcha fails, it retires with the new text generated on webpage"""
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
            handle_captcha()
    except:
        pass


def handle_class():
    """This medhod checks for 'online class' button, if it exists, it clicks on it or if there's error loading it,
    it repeats it by redirecting it to 1st process again."""
    time.sleep(3)
    try:
        online_class_button = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[1]/div[4]/div[1]/ul/li[9]/a')
        online_class_button.click()
    except:
        # handle_login()
        pass
        exit()

def get_timings():
    """get_timigs function checks the timings of the classes and it updates it in a timings.txt file"""
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
    """connect_to_zoom() function checks for the active online class button on online class webpage.
    if it finds it, it simulates a click on it and redirects to zoom page which will open the zoom app."""
    try:
        for i in range(1, 20):
            try:
                xpath = "/html/body/div[1]/div[3]/div[2]/div[1]/div/div/div[2]/div/div/div/div/div/div/div[2]/div[{}]/div/div/div[2]/a".format(i)
                active_class = driver.find_element_by_xpath(xpath)
                active_class.click()
                if active_class:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    driver.maximize_window()
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
        mouse.position = (830, 349) #this position needs to be updated as per the resolution of the system, and where the OS Alert box appears.
        mouse.click(Button.left, 1)
        time.sleep(5)
        driver.close()

if __name__ == '__main__':
    """for testing"""

    # driver = webdriver.Chrome(r"/home/froggy/Programs/Python/OnlineClass-Automation/ChromeDriver/chromedriver")
    try:
        open_webpage()
        time.sleep(2)
        enter_credentials()
        time.sleep(2)
        handle_captcha()
        time.sleep(2)
        handle_class()
        time.sleep(2)
        get_timings()
        connect_to_zoom()

    except:
        open_webpage()
        time.sleep(2)
        enter_credentials()
        time.sleep(2)
        handle_captcha()
        time.sleep(2)
        handle_class()
        time.sleep(2)
        get_timings()
        connect_to_zoom()
