#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
#
# utilidades para exportar anotaciones de pdfs guardados en ZOTERO
# Copyright © 2019 Valentín Basel <valentinbasel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import csv

import popplerqt4
import sys
import PyQt4

from os import scandir, getcwd
from os.path import abspath


def guardar_txt(texto,nombre_arch):
    """TODO: Docstring for guardar_txt.
    :returns: TODO

    """
    nombre_arch="/home/vbasel/RQDA/pdfs_txt/" + nombre_arch + ".txt"
    archivo_final = open(nombre_arch,"w")
    for datos in texto:
        #print(datos)
        archivo_final.write(datos+"\n")
    archivo_final.close()

def abrir_csv(archivo):
    """TODO: Docstring for abrir_csv.
    :returns: TODO

    """

    with open( archivo, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            autor =row["Author"].replace(",","_")
            autor = autor.replace(";","")
            autor = autor.replace(".","")
            autor = autor.replace(":","")
            titulo=row["Title"].replace(",","_")
            arch = row['File Attachments'].split(";")
            for datos in arch:
                if datos.find("pdf")>0:
                    pdf = datos#.replace(" ","\ ")
            nombre_arch=titulo.replace(" ","_")+"_"+autor.replace(" ","_")
            #nombre_arch , pdf
            notas = row["Notes"].replace("<p>","")
            #print(notas)
            leer_anot(pdf,nombre_arch,notas.replace("</p>",""))

def leer_anot(pdf,nombre_arch,notas_final):
    #print ("====================",notas_final)
    texto_final=[]
    texto_final.append("Notas:")
    texto_final.append(notas_final)
    texto_final.append("notas resaltadas de pdf:")
    try:
       doc = popplerqt4.Poppler.Document.load(pdf)
    except Exception as e:
        print("no se puede abrir el archivo")
        return False
    if doc==None:
        print("error al abrir el pdf")
        return False
    total_annotations = 0
    for i in range(doc.numPages()):

        page = doc.page(i)
        annotations = page.annotations()
        (pwidth, pheight) = (page.pageSize().width(), page.pageSize().height())
        if len(annotations) > 0:
            pagina=("pagina: {}".format(i+1))
            texto_final.append(pagina)
            for annotation in annotations:
                if  isinstance(annotation, popplerqt4.Poppler.Annotation):
                    total_annotations += 1
                    if(isinstance(annotation, popplerqt4.Poppler.HighlightAnnotation)):
                        quads = annotation.highlightQuads()
                        txt = ""
                        for quad in quads:
                            rect = (quad.points[0].x() * pwidth,
                                    quad.points[0].y() * pheight,
                                    quad.points[2].x() * pwidth,
                                    quad.points[2].y() * pheight)
                            bdy = PyQt4.QtCore.QRectF()
                            bdy.setCoords(*rect)
                            txt = txt + str(page.text(bdy)) + ' '

                        texto_final.append(txt)
                        texto_final.append("===")
    if total_annotations > 0 or notas_final != "":

        print ("se encontraron " + str(total_annotations)+" anotaciones en total")

        #print("###",texto_final)
        guardar_txt(texto_final,nombre_arch)
    else:
        print ("sin notas")
    #return texto_final



def main(args):
    arc_csv='/home/vbasel/RQDA/csv/RQDA.csv'
    abrir_csv(arc_csv)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

