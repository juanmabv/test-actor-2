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


timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

chr_options = webdriver.ChromeOptions()
chr_options.add_experimental_option('detach', True)

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chr_options, desired_capabilities=capa)

# -------------------------   SCE   -------------------------------------


verbose = True

ofertas = True

if ofertas:
    url_sce = "https://www.gobiernodecanarias.org/empleo/sce/principal/componentes/buscadores_angular/index_ofertas_empleo.jsp"

    lista_titulo = []
    lista_enlaces = []
    lista_fecha = []

    driver.get(url_sce)

    seguir = True
    while seguir:

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        # ESTO ES PARA IR BAJANDO Y QUE SALGAN
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(3)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        lista_resultados = []

        tiempo_reposo = 1

        while len(lista_resultados) == 0 and tiempo_reposo < 100:
            try:
                # driver.execute_script("document.body.style.zoom='75%'")
                lista_resultados = driver.find_elements(By.CSS_SELECTOR, 'div.article.ng-star-inserted')
                print(lista_resultados)
                prueba = 5 / len(lista_resultados)
            except:
                print(f'tiempo reposo: {tiempo_reposo}')
                time.sleep(tiempo_reposo)
                tiempo_reposo += 10

        pagina = 1
        print(f'página: {pagina}')

        for oferta in lista_resultados:
            if oferta == lista_resultados[-1]:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            else:
                pass

            time.sleep(1)
            titulo_oferta = oferta.find_element(By.CSS_SELECTOR, 'h6').get_attribute('innerText')
            lista_titulo.append(titulo_oferta)
            print(titulo_oferta) if verbose else 1

            fecha_oferta = oferta.find_element(By.CSS_SELECTOR, 'ul > li:nth-child(1)').get_attribute('innerText').split(': ')[-1]
            lista_fecha.append(fecha_oferta)
            print(fecha_oferta) if verbose else 1

            enlace_modal = oferta.find_element(By.CSS_SELECTOR, 'ul > li:nth-child(4) > a')
            enlace_modal.click()
            time.sleep(1)

            id_oferta = driver.find_element(By.CSS_SELECTOR, 'mat-dialog-content > table > tr:nth-child(1) > td:nth-child(2)').get_attribute('innerText')
            print(id_oferta) if verbose else 1

            enlace_oferta = f'https://www3.gobiernodecanarias.org/empleo/portal/web/sce/servicios/ofertas/ofertas_empleo/{id_oferta}'
            lista_enlaces.append(enlace_oferta)
            print(enlace_oferta) if verbose else 1

            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        n_paginas = int(driver.find_element(By.CSS_SELECTOR, 'ul.ngx-pagination > li.ng-star-inserted:nth-child(7)')
                        .get_attribute('innerText')
                        .split('\n')[-1])
        print(n_paginas)

        try:
            boton_siguiente = driver.find_element(By.CSS_SELECTOR,
                                                  'ul.ngx-pagination > li.ng-star-inserted:nth-child(8) > a')
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_element(By.CSS_SELECTOR, 'ul.ngx-pagination'))
            boton_siguiente.click()
            pagina += 1
        except:
            seguir = False
            print('no hay página siguiente')

    df_final = pd.DataFrame({
        'titulo': lista_titulo,
        'enlace': lista_enlaces,
        'fecha': lista_fecha,
    })

    df_final.to_csv(f'titulos_sce{timestamp}.csv', sep=';', index=False)

legacy_detalle_ofertas = True

if legacy_detalle_ofertas:
    df_enlaces = pd.read_csv(f'titulos_sce{timestamp}.csv', sep=';')

    lista_nombre = []

    lista_id = []
    lista_ubicacion = []
    lista_fecha_pub = []
    lista_vacantes = []

    lista_ett = []
    lista_discapacidad = []

    lista_nivel_profesional = []
    lista_experiencia = []
    lista_nivel_academico = []
    lista_titulacion = []
    lista_idiomas = []

    lista_informatica = []
    lista_otros_ctos = []
    lista_certif_prof = []
    lista_permisos_conducir = []
    lista_info_adicional = []

    for url_oferta in df_enlaces['enlace'].to_list():

        driver.get(url_oferta)
        time.sleep(1)
        driver.execute_script("window.stop();")
        time.sleep(3)

        try:
            wait = WebDriverWait(driver, 20)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body')))

            driver.execute_script("window.stop();")
        except:
            time.sleep(3)

        try:
            no_encontrado = driver.find_element(By.CSS_SELECTOR, 'body > div > div:nth-child(4) > div > a').get_attribute('innerText')
        except NoSuchElementException:

            nombre = driver.find_element(By.CSS_SELECTOR, '#ofertas_empleo > span').get_attribute('innerText')
            lista_nombre.append(nombre)

            elem_id = driver.find_element(By.CSS_SELECTOR,
                                          '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(1) > tbody > tr:nth-child(1) > td:nth-child(2)')
            id = elem_id.get_attribute('innerText')
            lista_id.append(id)

            elem_ubicacion = driver.find_element(By.CSS_SELECTOR,
                                                 '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(1) > tbody > tr:nth-child(2) > td:nth-child(2)')
            ubicacion = elem_ubicacion.get_attribute('innerText')
            lista_ubicacion.append(ubicacion)

            elem_fecha_pub = driver.find_element(By.CSS_SELECTOR,
                                                 '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(1) > tbody > tr:nth-child(3) > td:nth-child(2)')
            fecha_pub = elem_fecha_pub.get_attribute('innerText')
            lista_fecha_pub.append(fecha_pub)

            elem_vacantes = driver.find_element(By.CSS_SELECTOR,
                                                '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(1) > tbody > tr:nth-child(4) > td:nth-child(2)')
            vacantes = elem_vacantes.get_attribute('innerText')
            lista_vacantes.append(vacantes)

            print(f'{nombre} / {id}: bloque 1 listo') if verbose else 1

            elem_ett = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(2)')
            ett = elem_ett.get_attribute('innerText')
            lista_ett.append(ett)

            elem_discapacidad = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCurso > table:nth-child(3) > tbody > tr:nth-child(2) > td:nth-child(2)')
            discapacidad = elem_discapacidad.get_attribute('innerText')
            lista_discapacidad.append(discapacidad)

            print(f'{nombre} / {id}: bloque 2 listo') if verbose else 1

            elem_nivel_profesional = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(1) > td:nth-child(2)')
            nivel_profesional = elem_nivel_profesional.get_attribute('innerText')
            lista_nivel_profesional.append(nivel_profesional)

            elem_experiencia = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(2) > td:nth-child(2)')
            experiencia = elem_experiencia.get_attribute('innerText')
            lista_experiencia.append(experiencia)

            elem_nivel_academico = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(3) > td:nth-child(2)')
            nivel_academico = elem_nivel_academico.get_attribute('innerText')
            lista_nivel_academico.append(nivel_academico)

            elem_titulacion = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(4) > td:nth-child(2)')
            titulacion = elem_titulacion.get_attribute('innerText')
            lista_titulacion.append(titulacion)

            elem_idiomas = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(5) > td:nth-child(2)')
            idiomas = elem_idiomas.get_attribute('innerText')
            lista_idiomas.append(idiomas)

            print(f'{nombre} / {id}: bloque 3 listo') if verbose else 1

            elem_informatica = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(7) > td:nth-child(2)')
            informatica = elem_informatica.get_attribute('innerText')
            lista_informatica.append(informatica)

            elem_otros_ctos = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(8) > td:nth-child(2)')
            otros_ctos = elem_otros_ctos.get_attribute('innerText')
            lista_otros_ctos.append(otros_ctos)


            elem_certif_prof = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(9) > td:nth-child(2)')
            certif_prof = elem_certif_prof.get_attribute('innerText')
            lista_certif_prof.append(certif_prof)

            elem_permisos_conducir = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(10) > td:nth-child(2)')
            permisos_conducir = elem_permisos_conducir.get_attribute('innerText')
            lista_permisos_conducir.append(permisos_conducir)

            elem_info_adicional = driver.find_element(By.CSS_SELECTOR,
                                           '#cuerpo_detalle > ul.listadodatosCursoConPunto > table > tbody > tr:nth-child(11) > td:nth-child(2)')
            info_adicional = elem_info_adicional.get_attribute('innerText')
            lista_info_adicional.append(info_adicional)

            print(f'{nombre} / {id}: bloque 4 listo') if verbose else 1


    df_detalle_ofertas = pd.DataFrame({
        'nombre': lista_nombre,
        'id': lista_id,
        'ubicacion': lista_ubicacion,
        'fecha_pub': fecha_pub,
        'vacantes': lista_vacantes,
        'ett': lista_ett,
        'discapacidad': lista_discapacidad,
        'nivel_profesional': nivel_profesional,
        'experiencia': lista_experiencia,
        'nivel_academico': lista_nivel_academico,
        'titulacion': lista_titulacion,
        'idiomas': lista_idiomas,
        'ctos_informatica': lista_informatica,
        'otros_ctos': lista_otros_ctos,
        'certif_prof': lista_certif_prof,
        'permisos_conducir': lista_permisos_conducir,
        'info_adicional': lista_info_adicional,
    })

    df_detalle_ofertas['timestamp'] = datetime.datetime.now()
    df_detalle_ofertas.to_csv(f'detalle_ofertas_sce{timestamp}.csv', sep=';', index=False)
