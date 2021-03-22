from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.options import Options

'''
binary = FirefoxBinary("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r"geckodriver-v0.29.0-win64/geckodriver.exe")
try:
    driver.get('https://www.youtube.com/')
    html_content = driver.page_source  # ok e ovoa
except TimeoutError:
    print("nz veke so")
driver.quit()
'''

from urllib.request import urlopen, Request

f = urlopen(Request('https://www.gov.si/', headers={'User-Agent': 'fri-wier-obidzuko'}), timeout=10)
htmlStatusCode = f.getcode()
print(htmlStatusCode)
