from urllib.parse import urljoin

from apify import Actor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import pandas as pd

import datetime
import time
import math

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# To run this Actor locally, you need to have the Selenium Chromedriver installed.
# https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/
# When running on the Apify platform, it is already included in the Actor's Docker image.


async def main():
    async with Actor:
        # Read the Actor input
        actor_input = await Actor.get_input() or {}
        start_json = actor_input.get('start_json')

        if not start_json:
            Actor.log.info(
                'No start URLs specified in actor input, exiting...')
            await Actor.exit()

        # Launch a new Selenium Chrome WebDriver
        Actor.log.info('Launching Chrome WebDriver...')
        chrome_options = ChromeOptions()
        # if Actor.config.headless:
        #     chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('detach', True)
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"

        driver = webdriver.Chrome(
            options=chrome_options, desired_capabilities=capa)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

        try:

            for _, row in start_json.iterrows():
                data_dict = row.to_dict()
                print(data_dict)
                print(type(data_dict))

            # data = {
            #     'booleano': [True, False, False, True, True, False, False, True, False, False, True, False, True, False, True],
            #     'texto': ['Hola', 'Mundo', 'Python', 'Data', 'Science', 'OpenAI', 'ChatGPT', 'Pandas', 'DataFrame', 'Ejemplo', 'Columna', 'Número', 'Fecha', 'Hora', 'Datetime'],
            #     'entero': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            #     'decimal': [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11.1, 12.2, 13.3, 14.4, 15.5],
            #     'fecha': pd.date_range('2023-01-01', periods=15),
            #     'hora': pd.date_range('00:00:00', periods=15, freq='H'),
            #     'fecha_hora': pd.date_range('2023-01-01 00:00:00', periods=15, freq='H')
            # }

            # df = pd.DataFrame(data)

            # for _, row in df.iterrows():
            #     data_dict = row.to_dict()
            #     await Actor.push_data(data_dict)
        except:
            Actor.log.exception(f'Cannot extract data from {url}.')

        driver.quit()
