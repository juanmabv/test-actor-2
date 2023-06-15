import datetime
import time
import math

import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


import chromedriver_autoinstaller
chromedriver_autoinstaller.install()


timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

chr_options = webdriver.ChromeOptions()
chr_options.add_experimental_option('detach', True)

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(options=chr_options, desired_capabilities=capa)

url_start = 'https://www.latlong.net/convert-address-to-lat-long.html'

driver.get(url_start)

time.sleep(5)

bloque_cookies = driver.find_element(By.CSS_SELECTOR, "#onetrust-consent-sdk")

time.sleep(2)

driver.execute_script("document.getElementById('onetrust-consent-sdk').style.display='none';")

input_direccion = driver.find_element(By.CSS_SELECTOR, '#kN3709')
input_direccion.click()

time.sleep(1)

input_direccion. send_keys('Calle la noria 3, Santa Cruz de Tenerife, Spain')

time.sleep(2)

boton_enviar = driver.find_element(By.CSS_SELECTOR, '#btnfind')
boton_enviar.click()