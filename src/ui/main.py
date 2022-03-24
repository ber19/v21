import tkinter as tk
from tkinter import ttk, Tk, StringVar
from functools import partial
import traceback
from src.ui import functions as f
from src.utils import files
from src.variables import globales as varg
from src.scrapping.main import Navegador


class Window(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Descargar mallas")
        self.config(width=300, height=200)
        self.resizable(False, False)
        self.protocol()
        self.protocol("WM_DELETE_WINDOW", partial(f.on_closing, self))

    def first_view(self):
        try:
            self.lab1 = ttk.Label(self, text="Responsable:")
            self.lab1.place(x=60,y=30)

            lines = files.read_txt(varg.utils_path, "responsables.txt")
            responsables = [line.strip() for line in lines if "serv" in line.lower()] # EN EL ARCHIVO reponsables.txt
                                                                                      # SE TOMARAN EN CUENTA LOS QUE CONTENGAN "serv" (servicing)
                                                                                      
            self.resp = ttk.Combobox(
                self, values=responsables, justify=tk.CENTER,
                state="readonly")
            self.resp.place(x=60, y=55, width=180)
            self.resp.set("-- seleccionar --")
            self.btn_cont = ttk.Button(self, text="Continuar")
            self.btn_cont.place(x=110, y=120)
            self.btn_cont.config(command=partial(f.set_resp, lines, self.resp, self))
        except TypeError:
            if varg.selenium_driver:
                varg.selenium_driver.quit()
            # traceback.print_exc()
            self.lab1.destroy()
            self.show_ventana_err1()

    def second_view(self):
        self.lab1.destroy()
        self.resp.destroy()
        self.btn_cont.destroy()
        self.lab2 = ttk.Label(self, text="Descargando Mallas...\n"\
            "{}".format(varg.responsable))
        self.lab2.place(x=60, y=60)
        self.m = ttk.Label(textvariable=varg.malla_actual)
        self.m.place(x=80, y=110)
    
    def third_view(self):
        self.lab2.destroy()
        self.m.destroy()
        self.finish = ttk.Label(self, text="Proceso finalizado\n"\
            "{}".format(varg.responsable))
        self.finish.place(x=80, y=50)
        path = StringVar()
        self.path = tk.Entry(
            width=35,
            textvariable=path,
            state="readonly"
            )
        self.path.place(x=50, y=100)
        path.set(varg.mallas_path)

    def show_ventana(self):
        varg.nav = Navegador()
        varg.malla_actual = StringVar()
        self.first_view()
        self.mainloop()

#-------------

    def show_ventana_err(self):
        self.lab3 = ttk.Label(self, text="No se encontro la carpeta CarpetaTres\n"\
            "o el archivo path_mallas.txt")
        self.lab3.place(x=50, y=70)
        self.mainloop()

    def show_ventana_err7(self):
        self.lab9 = ttk.Label(self, text="Por favor, revise que el contenido de\n"\
            "path_mallas.txt sea una ruta valida")
        self.lab9.place(x=50, y=70)
        self.mainloop()
        
    def show_ventana_err1(self):
        self.lab4 = ttk.Label(self, text="No se encontro el archivo 'responsables.txt'")
        self.lab4.place(x=35, y=70)

    def show_ventana_err2(self):
        for w in self.winfo_children():
            w.destroy()
        self.lab6 = ttk.Label(self, text="No se puede realizar la conexion\n"\
            "con el scheduling. Revise su conexion a\n"\
                "internet, su VPN y sus credenciales\n"\
                    "en el archivo creds.txt")
        self.lab6.place(x=35, y=50)

    def show_ventana_err3(self):
        for w in self.winfo_children():
            w.destroy()
        self.lab7 = ttk.Label(self, text="No se encontro el archivo creds.txt")
        self.lab7.place(x=35, y=70)

    def show_ventana_err4(self, msg):
        for w in self.winfo_children():
            w.destroy()
        words = msg[msg.find("version"):msg.find("with")].split(" ")
        ver = ""
        for word in words:
            if "." in word: ver=word
        self.lab8 = ttk.Label(self, text="El chromedriver.exe no es compatible\n"\
            "con la version de su navegador\n\nVaya a este enlace y descargue\n"\
                "la version compatible con su navegador\n\t{}".format(ver))
        self.lab8.place(x=35, y=30)
        url = StringVar()
        url_driver = tk.Entry(
            width=40,
            textvariable=url,
            state="readonly"
        )
        url.set("https://chromedriver.chromium.org/downloads")
        url_driver.place(x=27, y=140)

    def show_ventana_err6(self):
        for w in self.winfo_children():
            w.destroy()
        self.lab5 = ttk.Label(self, text="No se encontro el chromedriver.exe\n"\
            "Descarguelo desde el siguiente enlace:")
        self.lab5.place(x=35, y=30)
        url = StringVar()
        url_driver = tk.Entry(
            width=40,
            textvariable=url,
            state="readonly"
        )
        url.set("https://chromedriver.chromium.org/downloads")
        url_driver.place(x=27, y=100)

    def show_ventana_err9(self):
        for w in self.winfo_children():
            w.destroy()
        self.lab11 = ttk.Label(self, text="Se cerro el proceso del navegador")
        self.lab11.place(x=35, y=40)
        










