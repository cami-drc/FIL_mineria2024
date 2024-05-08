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

neg_label = [atributos[i] for i in [1, 3, 6]]
pos_label = [atributos[i] for i in range(len(atributos)) if i not in [1, 3, 6]]
    
neg, pos = fnc.neg_pos(likert_limpio)  #separo datos en neg y pos

#%%

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4), sharey=True)

fig.suptitle("Preguntas Likert Charla 4", size="xx-large", weight="roman")

sns.violinplot(ax=ax1, data=pos, palette="colorblind")

ax1.set_xticks(ticks=range(len(pos_label)), labels=pos_label, rotation=45)

ax1.set_ylabel("Escala Likert (1-5)")
ax1.set_title("Atributos positivos")

sns.violinplot(ax=ax2, data=neg, palette="colorblind")

ax2.set_xticks(ticks=range(len(neg_label)), labels=neg_label, rotation=45)
ax2.set_title("Atributos negativos")

plt.show()

#%%

fnc.graph_neg_pos(likert_limpio, atributos)

#%%

## Calificacion general

calif_or = pd.read_csv("Charla4_calif.csv").values #saco los valores del csv

calif_limpio = fnc.clean(calif_or)

#%%

fig, ax = plt.subplots()

ax.set_title("Calificación general")

parts = ax.violinplot(calif_limpio, showmeans=False, showmedians=False,
showextrema=False, bw_method=0.4)

for pc in parts['bodies']:
    pc.set_facecolor("firebrick")
    pc.set_edgecolor("k")
    pc.set_alpha(1)

quartile1, medians, quartile3 = np.percentile(calif_limpio, [25, 50, 75], axis=0) #obtengo cuartiles

whiskers = np.array([fnc.adjacent_values(sorted_array, q1, q3)                  
    for sorted_array, q1, q3 in zip(calif_limpio, quartile1, quartile3)])

whiskers_min, whiskers_max = whiskers[:, 0], whiskers[:, 1]

inds = np.arange(1, len(medians) + 1)
ax.scatter(inds, medians, marker="o", color= "w", s=20, zorder=3)
ax.vlines(inds, quartile1, quartile3, color="k", linestyle='-', lw=7)
ax.vlines(inds, whiskers_min, whiskers_max, color="k", linestyle='-', lw=2)

#ax.yaxis.grid(True)

#fnc.set_axis_style(ax, "", "")

ax.set_yticks(np.arange((np.min(calif_limpio)-1), (np.max(calif_limpio)+1)))

ax.set_ylabel("Calificación (1-10)")

plt.show()