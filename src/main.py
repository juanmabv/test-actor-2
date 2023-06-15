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

            print(start_json)
            print(type(start_json))

            for item in start_json['input_json']:
                url_oferta = item['enlace']

                driver.get(url_oferta)
                time.sleep(1)
                driver.execute_script("window.stop();")
                time.sleep(3)

                try:
                    wait = WebDriverWait(driver, 20)

                    wait.until(EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'body')))

                    driver.execute_script("window.stop();")
                except:
                    time.sleep(3)

                # try:
                #     no_encontrado = driver.find_element(
                #         By.CSS_SELECTOR, 'body > div > div:nth-child(4) > div > a').get_attribute('innerText')
                # except NoSuchElementException:

                nombre = driver.find_element(
                    By.CSS_SELECTOR, '#ofertas_empleo > span').get_attribute('innerText')

                elem_id = driver.find_element(By.CSS_SELECTOR,
                                              '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(1) > tbody > tr:nth-child(1) > td:nth-child(2)')
                id = elem_id.get_attribute('innerText')

                elem_ubicacion = driver.find_element(By.CSS_SELECTOR,
                                                     '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(2)')
                ubicacion = elem_ubicacion.get_attribute('innerText')

                elem_fecha_pub = driver.find_element(By.CSS_SELECTOR,
                                                     '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(1) > tbody > tr:nth-child(3) > td:nth-child(2)')
                fecha_pub = elem_fecha_pub.get_attribute('innerText')

                elem_vacantes = driver.find_element(By.CSS_SELECTOR,
                                                    '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(1) > tbody > tr:nth-child(4) > td:nth-child(2)')
                vacantes = elem_vacantes.get_attribute('innerText')

                print(f'{nombre} / {id}: bloque 1 listo') if verbose else 1

                elem_ett = driver.find_element(By.CSS_SELECTOR,
                                               '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2)')
                ett = elem_ett.get_attribute('innerText')

                elem_discapacidad = driver.find_element(By.CSS_SELECTOR,
                                                        '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(2)')
                discapacidad = elem_discapacidad.get_attribute('innerText')

                print(f'{nombre} / {id}: bloque 2 listo') if verbose else 1

                elem_nivel_profesional = driver.find_element(By.CSS_SELECTOR,
                                                             '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(1) > td:nth-child(2)')
                nivel_profesional = elem_nivel_profesional.get_attribute(
                    'innerText')

                elem_experiencia = driver.find_element(By.CSS_SELECTOR,
                                                       '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(2) > td:nth-child(2)')
                experiencia = elem_experiencia.get_attribute('innerText')

                elem_nivel_academico = driver.find_element(By.CSS_SELECTOR,
                                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(3) > td:nth-child(2)')
                nivel_academico = elem_nivel_academico.get_attribute(
                    'innerText')

                elem_titulacion = driver.find_element(By.CSS_SELECTOR,
                                                      '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(4) > td:nth-child(2)')
                titulacion = elem_titulacion.get_attribute('innerText')

                elem_idiomas = driver.find_element(By.CSS_SELECTOR,
                                                   '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(5) > td:nth-child(2)')
                idiomas = elem_idiomas.get_attribute('innerText')

                print(f'{nombre} / {id}: bloque 3 listo') if verbose else 1

                elem_informatica = driver.find_element(By.CSS_SELECTOR,
                                                       '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(7) > td:nth-child(2)')
                informatica = elem_informatica.get_attribute('innerText')

                elem_otros_ctos = driver.find_element(By.CSS_SELECTOR,
                                                      '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(8) > td:nth-child(2)')
                otros_ctos = elem_otros_ctos.get_attribute('innerText')

                elem_certif_prof = driver.find_element(By.CSS_SELECTOR,
                                                       '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(9) > td:nth-child(2)')
                certif_prof = elem_certif_prof.get_attribute('innerText')

                elem_permisos_conducir = driver.find_element(By.CSS_SELECTOR,
                                                             '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(10) > td:nth-child(2)')
                permisos_conducir = elem_permisos_conducir.get_attribute(
                    'innerText')

                elem_info_adicional = driver.find_element(By.CSS_SELECTOR,
                                                          '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(11) > td:nth-child(2)')
                info_adicional = elem_info_adicional.get_attribute(
                    'innerText')

                print(f'{nombre} / {id}: bloque 4 listo') if verbose else 1

                await Actor.push_data({
                    "nombre": nombre,
                    "id": id,
                    "ubicacion": ubicacion,
                    "fecha_pub": fecha_pub,
                    "vacantes": vacantes,
                    "ett": ett,
                    "discapacidad": discapacidad,
                    "nivel_profesional": nivel_profesional,
                    "experiencia": experiencia,
                    "nivel_academico": nivel_academico,
                    "titulacion": titulacion,
                    "idiomas": idiomas,
                    "informatica": informatica,
                    "otros_ctos": otros_ctos,
                    "certif_prof": certif_prof,
                    "permisos_conducir": permisos_conducir,
                    "info_adicional": info_adicional
                })

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
