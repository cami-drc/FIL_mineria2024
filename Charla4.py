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