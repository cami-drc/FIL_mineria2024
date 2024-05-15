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

fnc.calif(calif_limpio)

#%%

## Demografía

demografia_or = pd.read_csv("Charla4_Demografia.csv").values #saco los valores del csv

#%%
data = demografia_or[:,1]

promedio = np.mean(data)
prom_red = round(promedio, 2)
cont = data.size

texto = "El número de respuestas es " +str(cont)+ " y el promedio es de " +str(prom_red)


sns.violinplot(data=data)
    
plt.subplots_adjust(top=0.9) #espacio adicional entre gráfica y título 

plt.xlabel('Participantes') #eje x título 
plt.ylabel('Edad (años)') #eje y título 
    
plt.text(0.5, 0.9, '', transform=plt.gca().transAxes)
plt.figtext(0.5, 0.02, texto, ha='center', fontsize=9) 
# pie de figura, los segundos valores es para moverlo en el eje y y el primero en x para centrarlo o no 
    
plt.title('Distribución de edad', y=1.05, pad=20, size="xx-large") # para que no slaga pegado a la gráfica el título 
    
plt.xticks(ticks=[], labels=['Participantes'])  # Eliminar las etiquetas del eje x y establecer solo 'Participantes'
    
plt.show()

#%%

fnc.edad_clean(data)
