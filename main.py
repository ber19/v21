import traceback
from typing import Type
from src.utils import clean_scrap, files
from src.variables import globales as varg
from os import path
from src.ui import main as ui
import os


def main():
    try:
        clean_scrap.clean_mei()
        clean_scrap.clean_drag()
        try:
            clean_scrap.clean_scoped()
        except PermissionError:
            pass
        os.system("taskkill /F /IM chromedriver.exe")
        
        varg.utils_path = path.join(path.expanduser('~'), "Documents", "CarpetaTres")
        varg.mallas_path = files.read_txt(varg.utils_path, "path_mallas.txt")[0]
        if not path.isdir(varg.mallas_path):
            raise AssertionError
        varg.ventana = ui.Window()
        varg.ventana.show_ventana()

    except AssertionError:
        varg.ventana = ui.Window()
        varg.ventana.show_ventana_err7()
    except TypeError:
        varg.ventana = ui.Window()
        varg.ventana.show_ventana_err()
    except Exception:
        if varg.selenium_driver:
            varg.selenium_driver.quit()
        traceback.print_exc()


if __name__ == "__main__":
    main()
        


















