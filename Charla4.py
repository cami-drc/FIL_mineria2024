#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 17:23:47 2024

@author: camiladelrio
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import funciones as fnc

#%%

## Likert

likert_or = pd.read_csv("Charla4_likert.csv").values #saco los valores del csv

likert_limpio = fnc.clean(likert_or) #limpio los datos

#%%

atributos = ["Gozo","Confusion","Expectativas","Lenguaje","Analogias",
             "Imagenes","Fluidez","Atencion","Gestos","Importancia","Interes"]

#%%

fnc.graph_neg_pos(likert_limpio, atributos, title="Preguntas Likert Charla 4")

#%%

## Calificacion general

calif_or = pd.read_csv("Charla4_calif.csv").values #saco los valores del csv

calif_limpio = fnc.clean(calif_or)

#%%

fnc.calif(calif_limpio, title="Calificación general Charla 4")

#%%

## Demografía

demografia_or = pd.read_csv("Charla4_Demografia.csv").values #saco los valores del csv

#%%
#Edad

edad = demografia_or[:,1]

edad = fnc.edad_clean(edad)

#%%

fnc.plot_edad(edad)

#%%
#Genero

generos = demografia_or[:,2]

#%%

fnc.plot_genero(generos)

#%%

ocupacion = demografia_or[:,3]
#%%

ocupacion_limpio = np.array(['NaN' if isinstance(x, float) and np.isnan(x) else x for x in ocupacion])

valores_unicos, conteos = np.unique(ocupacion_limpio, return_counts=True)

#%%

plt.figure(figsize=(8, 6))
plt.pie(conteos, labels=valores_unicos, autopct=fnc.autopct_format(conteos), startangle=90, colors=['blue', 'orange', 'green', 'red'])

# Añadir título
plt.title('Distribución de Ocupaciones')

# Mostrar la gráfica
plt.show()