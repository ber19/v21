from src.variables import globales as varg
import os
from os import path
import re
import time
from src.datos import datos
from datetime import datetime

def get_files_paths():
    files = [path.splitext(path.join(varg.m_path, f)) \
        for f in os.listdir(varg.m_path) \
            if path.isfile(path.join(varg.m_path, f))]
    xmls = [x for x in files if x[1].lower() == ".xml"]
    mallas = [m for m in xmls if re.search("^CR-MX.+-T02$", path.basename(m[0]))]
    return mallas

# def remove_old(malla):
#     for m in get_files_paths():
#         if malla.upper() == path.basename(m[0]).upper():
#             os.remove(m[0] + m[1])
#             break

def check_download(malla):
    while True:
        mallas = get_files_paths()
        for m in mallas:
            if path.basename(m[0]).upper() == malla.upper():
                return True
        time.sleep(2)

def create_folder():
    if not path.exists(path.join(varg.mallas_path, varg.responsable)):
        os.makedirs(path.join(varg.mallas_path, varg.responsable))
    varg.m_path = path.join(varg.mallas_path, varg.responsable)
    for file_name in os.listdir(varg.m_path):
        file = path.join(varg.m_path, file_name)
        if path.isfile(file):
            os.remove(file)

def read_txt(dir, file_name):
    path_txt = path.join(dir, file_name)
    if path.exists(path_txt):
        with open(path.join(dir, file_name)) as f:
            return [line.strip() for line in f.readlines() if len(line.strip()) > 0]
    else:
        pass
        ## APARECERA MENSAJE DICIENDO QUE EL ARCHIVO NO EXISTE

def create_text(ruta, file):
    text = "{}\n\n".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    for malla, data in datos.datos_malla_sched.items():
        text = text +  malla + ":"
        # print(malla)
        # print(data)
        for i in range(1, len(data)):
            if i == 1: text = text + "\n" + "FOLDER:\n" + data[i]
            if i == 2: text = text + "\n" + "DAILY:\n" + data[i]
            if i == 3: text = text + "\n" + "FECHA ULTIMO DESPLIEGUE:\n" + data[i]
            if i == 4: text = text + "\n" + "FECHA ULTIMA MODIFICACION:\n" + data[i]
            if i == 5: text = text + "\n" + "VERSION:\n" + data[i] + "\n"
        text = text + "-"*19 + "\n"
    with open(path.join(ruta, file), "w") as f:
        f.write(text)



















