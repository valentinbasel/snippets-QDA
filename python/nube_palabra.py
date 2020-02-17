#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###############################################################################
# función para crear nubes de palabras a partir de un archivo Txt.
# Copyright © 2020 Valentin Basel <valentinbasel@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################

import re
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from wordcloud import WordCloud
from collections import Counter


def crear_nube(arch, nuevas_palabras_vacias):
    """
    arch : String con la ruta completa del txt a analizar
            ej: '/home/user/archivo_texto.txt'
    nuevas_palabras_vacias : lista de strings con las palabras que el sistema
                              no reconocera
                              ej: ['false','default']
    paso del algoritmo:
    1- carga el archivo txt
    2- carga las palabras a evitar (stopword + nuevas_palabras_vacias)
    3- busca el patron de coincidencia de las palabras
    4- crea diccionario con las palabras y su frecuencia
    5- crea nube de palabras
    6- guarda nube de palabras en arch+'png'
    return True
    """
    documento = open(arch, 'r')
    # declarar palabras vacías - stopwords en español
    palabras_vacias = set(stopwords.words('spanish'))
    # adicionar otras palabras vacías si es el caso

    palabras_vacias = set(palabras_vacias.union(nuevas_palabras_vacias))
    # diccionario que recibirá las palabras del texto y su frecuencia
    frecuencia_palabras = {}
    # convertir el documento en minúsculas
    texto = documento.read().lower()
    # solo ver caracteres alfabéticos y vocales con acento
    patron_coincidencia = re.findall(r'\b[a-z,á,é,í,ó,ú,ñ]{3,20}\b', texto)
    # eliminar las palabras vacías
    patron_coincidencia = [word for word in patron_coincidencia
                           if word not in palabras_vacias]
    # generar el diccionario con la fercuencia de palabras
    for palabra in patron_coincidencia:
        cantidad = frecuencia_palabras.get(palabra, 0)
        frecuencia_palabras[palabra] = cantidad + 1
    # preparar el diccionario para la nube de palabras
    nube_palabras_diccionario = Counter(frecuencia_palabras)
    # configurar y generar la nube de palabras sin máscara
    nube_palabras = WordCloud(width=1200, height=1200,
                              background_color="white",
                              max_words=800,
                              contour_width=20,
                              contour_color='steelblue')
    nube_palabras.generate_from_frequencies(nube_palabras_diccionario)
    # mostrar la nube de palabras
    plt.figure(figsize=(15, 8))
    plt.imshow(nube_palabras)
    plt.axis("off")
    keys = nube_palabras_diccionario.keys()
    archivo_csv = open(arch+".csv", "w")
    for a in keys:
        cadena = a + "," + str(nube_palabras_diccionario[a]) + "\n"
        archivo_csv.write(cadena)
    archivo_csv.close()
    # guardar la nube de palabras en una imagen
    nube_palabras.to_file(arch+".png")
    return True
