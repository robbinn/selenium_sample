from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

file = open('path.txt', 'r')
lines = file.readlines()

torexe = os.popen(lines[0].strip())  # full path for tor.exe
binary = FirefoxBinary(lines[1].strip())  # full path for firefox.exe
profile = FirefoxProfile(lines[2].strip())  # full path for profile.default
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.update_preferences()
service = Service(lines[3].strip())  # full path for geckodriver.exe
driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=profile,
                           service=service)

# dark fox seed url
baseurl = 'http://57d5j6bbwlpxbxe5tsjjy3vziktv3fo2o5j3nheo4gpg6lzpsimzqzid.onion'
driver.get(baseurl)

# wait for captcha page show up
WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div/div/form/button[1]")))

# save captcha to local
driver.find_element(by=By.XPATH, value="/html/body/div/div/form/div[1]/div[1]").screenshot("captcha.png")

# wait until input space show up
inputBox = driver.find_element(by=By.XPATH, value="/html/body/div/div/form/div[1]/div[2]/input")

# ask user input captha solution in terminal
userIn = input("Enter solution: ")

# send user solution into the input space
inputBox.send_keys(userIn)

# click the verify(submit) button
driver.find_element(by=By.XPATH, value="/html/body/div/div/form/button[1]").click()

# wait for listing page show up (This Xpath may need to change based on different seed url)
WebDriverWait(driver, 100).until(EC.visibility_of_element_located(
    (By.XPATH, "/html/body/main/div/div/div[2]/div[2]/div/div[2]/article[1]/div/div[2]/div[2]/div/a")))

# below for testing purpose only
links = driver.find_elements(by=By.CLASS_NAME, value="media-content")
print("There are " + str(len(links)) + " urls found.", end='\n')

# print titles for each listing
for link in links:
    print(link.find_element(by=By.CSS_SELECTOR, value='p.title.is-5').text)
