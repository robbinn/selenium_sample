from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.service import Service
import os
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


# Saves the crawled html page
def savePage(seleniumDriver, url):
    filePath = getFullPathName(url)
    os.makedirs(os.path.dirname(filePath), exist_ok=True)
    with open(filePath, "w", encoding="utf-8") as f:
        f.write(seleniumDriver.page_source)
    return


# Returns True if the link is 'Topic' Links
def isDescriptionLink(url):
    if 'topic' in url:
        return True
    return False


# Gets the full path of the page to be saved along with its appropriate file name
def getFullPathName(url):
    fileName = getNameFromURL(url)
    if isDescriptionLink(url):
        fullPath = '../selenium/HTML_Pages/' + str("%02d" % date.today().month) + str(
            "%02d" % date.today().day) + str("%04d" % date.today().year) + '/' + 'Description/' + fileName + '.html'
    else:
        fullPath = '../selenium/HTML_Pages/' + str("%02d" % date.today().month) + str(
            "%02d" % date.today().day) + str("%04d" % date.today().year) + '/' + 'Listing/' + fileName + '.html'
    return fullPath


# Creates the name of the file based on URL
def getNameFromURL(url):
    global counter
    name = ''.join(e for e in url if e.isalnum())
    if (name == ''):
        name = str(counter)
        counter = counter + 1
    return name


file = open('path.txt', 'r')
lines = file.readlines()

torexe = os.popen(lines[0].strip())  # path for tor.exe
binary = FirefoxBinary(lines[1].strip())  # full path for firefox.exe
profile = FirefoxProfile(lines[2].strip())  # full path for profile.default
service = Service(lines[3].strip())  # full path for geckodriver.exe
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.socks', '127.0.0.1')
profile.set_preference('network.proxy.socks_port', 9050)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.update_preferences()
# options = Options()
# options.headless = True
driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=profile,
                           service=service)

# Best Carding world seed url
driver.get('http://bestteermb42clir6ux7xm76d4jjodh3fpahjqgbddbmfrgp4skg2wqd.onion/viewforum.php?f=47')

# Wait until topic show up
WebDriverWait(driver, 100).until(
    EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[3]/div/ul[2]/li[1]/dl/dt/div/a")))

while True:
    links = driver.find_elements(by=By.CLASS_NAME, value='topictitle')
    for link in links:
        full_url = link.get_attribute("href")
        print(full_url)
        driver.get(full_url)
        WebDriverWait(driver, 100).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/h2/a")))
        savePage(driver, full_url)
        driver.back()
        WebDriverWait(driver, 100).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div[3]/div/ul[2]/li[1]/dl/dt/div/a")))
    try:
        driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[2]/div[3]/ul/li[3]/a').click()
    except NoSuchElementException:
        break

print("Done!")
