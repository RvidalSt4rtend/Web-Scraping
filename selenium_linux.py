from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import sys

def initialize_driver():
    chrome_options = Options()
    #Comment the headless option if you want to see the browser
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage") 
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36")

    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    driver_path = os.path.join(base_path, 'chromedriver')
    return webdriver.Chrome(service=Service(driver_path), options=chrome_options)

def search_currency(driver, currency_name):
    try:
     
        descripcion = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/form/center/table/tbody/tr[2]/td/table/tbody/tr[2]/td/center/table/tbody/tr[5]/td[2]/input'))
        )
        submit = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/form/center/table/tbody/tr[3]/td/div/font/input[1]'))
        )
        

        descripcion.click()
        descripcion.send_keys(currency_name)
        submit.click()

        # Esperar y obtener el valor de aduanas
        valor_aduanas = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/form/center[2]/table/tbody/tr[1]/td/table[3]/tbody/tr/td/table/tbody/tr[2]/td[4]'))
        ).text
        print(f"Valor en Aduanas {currency_name}:", valor_aduanas)
        return valor_aduanas

    except Exception as e:
        print(f"Error al obtener los datos para {currency_name}:", e)
        return None

def go_back(driver):
    try:
        # Regresar a la página de búsqueda
        regresar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/form/center[2]/table/tbody/tr[2]/td/table/tbody/tr/td/a'))
        )
        regresar.click()
    except Exception as e:
        print("Error al regresar a la página anterior:", e)

def search_currency2(driver):
    currency_name = "DOLAR"
    try:
        # Esperar a que el campo de descripción y el botón de envío estén disponibles
        tipo_cambio_venta = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/section[2]/div/div/div[2]/section/div[2]/div/div[1]/strong'))
        ).text
        tipo_cambio_penta = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/section[2]/div/div/div[2]/section/div[2]/div/div[2]/strong'))
        ).text
        print(f"Precio de Venta {currency_name}:", tipo_cambio_venta)
        print(f"Precio de Compra {currency_name}:", tipo_cambio_penta)
    except Exception as e:
        print("Error al obtener los datos:", e)

def main():
    url = "https://ww3.sunat.gob.pe/cl-ad-ittipocambioconsulta/TipoCambioS01Alias?accion=consultarTipoCambio"
    url2= "https://www.sunat.gob.pe/"
    
    driver = initialize_driver()
    driver.get(url)

    # Lista de monedas a buscar
    currencies = ["SWISS FRANC", "EURO"]

    for currency in currencies:
        search_currency(driver, currency)
        go_back(driver)
    driver.quit()

    driver = initialize_driver()
    driver.get(url2)
    search_currency2(driver)



if __name__ == "__main__":
    main()
