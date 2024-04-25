#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 17:23:47 2024

@author: camiladelrio
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import funciones as fnc

#%%

likert_or = pd.read_csv("Charla4_Likert.csv").values #saco los valores del csv

likert_limpio = fnc.clean(likert_or) #limpio los datos

#%%

atributos = ["Gozo","Confusion","Expectativas","Lenguaje","Analogias",
             "Imagenes","Fluidez","Atencion","Gestos","Importancia","Interes"]

#%%

fnc.graph_neg_pos(likert_limpio, atributos,  #grafico pos y neg
                  med_s=80)