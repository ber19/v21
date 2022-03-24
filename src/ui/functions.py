from src.variables import globales as varg
from src.utils import files
import sys

def on_closing(ventana):
    if varg.selenium_driver:
        varg.nav.join()
        varg.selenium_driver.quit()
    ventana.destroy()
    sys.exit()

def check(vent):
    if varg.nav.is_alive():
        vent.after(500, check, vent)
    else:
        if not varg.error:
            vent.third_view()       

def set_resp(lines, combo, vent):
    resp = combo.get()
    if resp == "-- seleccionar --":
        return
    varg.responsable = combo.get()
    files.create_folder()
    uuaas = []
    flag1 = False
    for line in lines:
        if line.strip() == varg.responsable:
            flag1 = True
            continue
        if "serv" in line.lower() and flag1:
            break
        if flag1:
            uuaas.append(line.strip()[1:])
    varg.uuaas = uuaas
    varg.nav.start() ## varg.nav -> ES EL THREAD
    vent.second_view()
    check(vent)



        



    



