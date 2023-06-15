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
        start_urls = actor_input.get('start_urls')
        max_depth = actor_input.get('max_depth')
        prueba_input = actor_input.get('prueba_input')

        if not start_urls:
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

            driver.get(start_urls[0]['url'])

            verbose = True

            ofertas = True

            if ofertas:
                url_sce = "https://www.gobiernodecanarias.org/empleo/sce/principal/componentes/buscadores_angular/index_ofertas_empleo.jsp"

                lista_titulo = []
                lista_enlaces = []
                lista_fecha = []

                driver.get(url_sce)
                pagina = 0

                seguir = True
                while seguir:

                    # Get scroll height
                    last_height = driver.execute_script(
                        "return document.body.scrollHeight")

                    # ESTO ES PARA IR BAJANDO Y QUE SALGAN
                    while True:
                        # Scroll down to bottom
                        driver.execute_script(
                            "window.scrollTo(0, document.body.scrollHeight);")

                        # Wait to load page
                        time.sleep(3)

                        # Calculate new scroll height and compare with last scroll height
                        new_height = driver.execute_script(
                            "return document.body.scrollHeight")
                        if new_height == last_height:
                            break
                        last_height = new_height

                    lista_resultados = []

                    tiempo_reposo = 1

                    while len(lista_resultados) == 0 and tiempo_reposo < 100:
                        try:
                            # driver.execute_script("document.body.style.zoom='75%'")
                            lista_resultados = driver.find_elements(
                                By.CSS_SELECTOR, 'div.article.ng-star-inserted')
                            print(lista_resultados)
                            prueba = 5 / len(lista_resultados)
                        except:
                            print(f'tiempo reposo: {tiempo_reposo}')
                            time.sleep(tiempo_reposo)
                            tiempo_reposo += 10

                    print(f'página: {pagina}')

                    for oferta in lista_resultados:
                        if oferta == lista_resultados[-1]:
                            driver.execute_script(
                                "window.scrollTo(0, document.body.scrollHeight);")
                        else:
                            pass

                        time.sleep(1)
                        titulo_oferta = oferta.find_element(
                            By.CSS_SELECTOR, 'h6').get_attribute('innerText')
                        print(titulo_oferta) if verbose else 1

                        fecha_oferta = oferta.find_element(
                            By.CSS_SELECTOR, 'ul > li:nth-child(1)').get_attribute('innerText').split(': ')[-1]
                        print(fecha_oferta) if verbose else 1

                        enlace_modal = oferta.find_element(
                            By.CSS_SELECTOR, 'ul > li:nth-child(4) > a')
                        enlace_modal.click()
                        time.sleep(1)

                        id_oferta = driver.find_element(
                            By.CSS_SELECTOR, 'mat-dialog-content > table > tr:nth-child(1) > td:nth-child(2)').get_attribute('innerText')
                        print(id_oferta) if verbose else 1

                        enlace_oferta = f'https://www3.gobiernodecanarias.org/empleo/portal/web/sce/servicios/ofertas/ofertas_empleo/{id_oferta}'
                        print(enlace_oferta) if verbose else 1

                        await Actor.push_data({'enlace': enlace_oferta, 'fecha': fecha_oferta, 'titulo': titulo_oferta})

                        webdriver.ActionChains(driver).send_keys(
                            Keys.ESCAPE).perform()

                    n_paginas = int(driver.find_element(By.CSS_SELECTOR, 'ul.ngx-pagination > li.ng-star-inserted:nth-child(7)')
                                    .get_attribute('innerText')
                                    .split('\n')[-1])
                    pagina += 1
                    print(f'Página {pagina} de {n_paginas}')

                    try:
                        boton_siguiente = driver.find_element(By.CSS_SELECTOR,
                                                              'ul.ngx-pagination > li.ng-star-inserted:nth-child(8) > a')
                        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(
                            By.CSS_SELECTOR, 'ul.ngx-pagination'))
                        boton_siguiente.click()
                        pagina += 1
                    except:
                        seguir = False
                        print('no hay página siguiente')

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
