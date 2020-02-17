#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import html2text
import os


def tranformar_txt(path_final, ruta_guardar, nombre_arch):
    files = []
    # r=root, d=directories, f = files
    nombre = []
    raiz = []
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    for r, d, f in os.walk(path_final):

        for file in f:
            if '.html' in file:
                files.append(os.path.join(r, file))
                nombre.append(file)
                raiz.append(r)
    texto = ""
    texto_html = ""
    for f in files:
        arch = open(f, "r")
        print(f)
        for linea in arch:
            texto_html = texto_html + linea
        texto += h.handle(texto_html)
    try:
        archivo_final = open(ruta_guardar + "/"+nombre_arch + ".txt", "w")
        for dato in texto:
            archivo_final.write(dato)
        archivo_final.close()
    except Exception as e:
        raise e


def recolector_url(path_final):
    """TODO: Docstring for recolector_url.
    :returns: TODO

    """
    cad_wget = 'wget --limit-rate=200k --no-clobber --convert-links'\
        + ' -r -E -e robots=off -U -A -P '\
        + path_final + ' html --domain='+ruta+' http://'+ruta
    os.system(cad_wget)


ruta_guardar = "/home/vbasel/"
ruta = "tecnokids.com"
path = os.getcwd() + "/"\
        + os.path.join(os.path.dirname(__file__)) + "/paginas_descargadas"
path_final = path+ruta

# recolector_url(path_final)

tranformar_txt(path_final, ruta_guardar, ruta)

##scriptpath = os.path.realpath(__file__)
#cadena_txt=path+"txt_html/"+ruta+".txt"
#R = "Rscript " +os.getcwd()+"/"+os.path.join(os.path.dirname(__file__))+ "/nube_palabras_sin_RQDA.r "+cadena_txt
#print(R)
#os.system(R)
#ruta="www.inteligenciaeducativa.net"
#ruta="educabot.org"
#ruta="robotgroup.com.ar"
#ruta="laescuelamaker.com"
#ruta = "www.cursovideojuegos.com.ar"

