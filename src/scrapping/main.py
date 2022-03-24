from lib2to3.pgen2 import driver
from threading import Thread
from selenium import webdriver
from src.variables import globales as varg
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException, \
    InvalidSessionIdException, SessionNotCreatedException, \
        NoSuchWindowException
from requests.exceptions import ConnectionError
from os import path
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW
from src.utils import files
from src.datos import datos
from threading import Thread



class Navegador(Thread): ## EL HILO
    def __init__(self):
        super().__init__()

    def aux1(self, driver):
        for uuaa in varg.uuaas:
            for per in varg.periodicidades:
                malla = "CR-MX{}{}-T02".format(uuaa, per)
                flr_box = driver.find_element_by_id("malla")
                flr_box.clear()
                flr_box.send_keys(malla)
                buscar = driver.find_element_by_id("Buscar")
                buscar.click()
                driver.find_elements_by_id("tblEjec")
                soup = BeautifulSoup(driver.page_source, "html.parser")
                table = soup.find("table", attrs={"id":"tblEjec"})
                if table.find_all("tr")[1:]:
                    varg.malla_actual.set(malla)
                    for row in table.find_all("tr")[1:]:
                        datos.datos_malla_sched[malla] = [value.getText() for value in row.find_all("td")]
                    dwn_xml = driver.find_element_by_xpath("//input[@value='Descargar XML']")
                    # files.remove_old(malla)
                    dwn_xml.click()
                    files.check_download(malla)
                else:
                    continue
        varg.selenium_driver.quit()
        varg.selenium_driver = None
        files.create_text(varg.m_path, "Info_mallas.txt")
        # print(datos.datos_malla_sched) ## ** PARA VER LOS DATOS DE LAS MALLAS DESCARGADAS

    def run(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            options.add_experimental_option("prefs", {
                "download.default_directory": varg.m_path, # NO NECESITA try
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing_for_trusted_sources_enabled": False,
                "safebrowsing.enabled": False
            })
            options.add_argument("--headless")
            options.add_argument("--window-size=1280x720")
            try: # err6
                service = Service(path.join(varg.utils_path, "chromedriver.exe"))
                service.creationflags = CREATE_NO_WINDOW
                varg.selenium_driver = webdriver.Chrome(
                options=options, service=service)
            except SessionNotCreatedException as err:
                varg.error = True
                varg.ventana.show_ventana_err4(err.msg)
                return
            except WebDriverException:
                varg.error = True
                varg.ventana.show_ventana_err6()
                return
            varg.selenium_driver.get(varg.URL_DOWNLOADXML)
            varg.selenium_driver.implicitly_wait(5)
            usr_box = varg.selenium_driver.find_element_by_id("j_username")
            varg.ctrlm_user = files.read_txt(varg.utils_path, "creds.txt")[0]
            usr_box.send_keys(varg.ctrlm_user)
            pwd_box = varg.selenium_driver.find_element_by_id("j_password")
            varg.ctrlm_pwd = files.read_txt(varg.utils_path, "creds.txt")[1]
            pwd_box.send_keys(varg.ctrlm_pwd)
            sign_in = varg.selenium_driver.find_element_by_id("Consultar")
            sign_in.click()
            varg.selenium_driver.find_element_by_class_name('isa_success')
            varg.selenium_driver.get(varg.URL_DOWNLOADXML)
            self.aux1(varg.selenium_driver)
        except InvalidSessionIdException:
            pass
        except NoSuchWindowException:
            varg.error = True
            varg.ventana.show_ventana_err9()
        except ConnectionError: # err2 | atrapa cuando no esta la vpn
            varg.error = True
            varg.ventana.show_ventana_err2()
        except TypeError: # err3
            varg.error = True
            varg.ventana.show_ventana_err3()
        except SessionNotCreatedException as err: # err4
            varg.error = True
            varg.ventana.show_ventana_err4(err.msg)
        except WebDriverException: # err2 | atrapa cuando no hay internet
            varg.error = True
            varg.ventana.show_ventana_err2()            
        finally:
            if varg.selenium_driver:
                varg.selenium_driver.quit()
          










