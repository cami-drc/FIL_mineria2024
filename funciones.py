#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:54:51 2024

@author: camiladelrio
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%

#Limpiar datos

def remove_nan(data):
    """
    Función para quitar las filas y columnas que tienen puro nan

    Parameters
    ----------
    data : array
        datos no limpios.

    Returns
    -------
    no_nan : array
        datos sin columnas y filas con puro nan.

    """
    cols_all_nan = np.all(np.isnan(data), axis=0)
    rows_all_nan = np.all(np.isnan(data), axis=1) 

    no_nan = data[:, ~cols_all_nan]
    no_nan = no_nan[~rows_all_nan, :]
    
    return no_nan


def remove_id(data):
    """
    Para quitar la primer columna, que contiene los índices (id de respuesta)

    Parameters
    ----------
    data : array
        datos con columna con id.

    Returns
    -------
    no_index : array
        array sin la columna con id.

    """
   
    no_id = data[:, 1:]
    return no_id

def clean_data(data):
    """
    Para quitar las filas (respuestas individuales) que no respondieron todas las preguntas

    Parameters
    ----------
    data : array
        datos ya sin id ni columnas/filas vacías.

    Returns
    -------
    clean_data : array
        datos limpios.

    """
    # Identificar las filas que tienen al menos un nan
    rows_with_nan = np.any(np.isnan(data), axis=1) 

    # Obtener las filas que no contienen ningún nan
    clean_data = data[~rows_with_nan]
    
    return clean_data

def clean(data):
    """
    Función completa de limpieza de datos. Elimina las columnas y filas vacías, la columna de id
    y las filas (respuestas individuales) que no respondieron todas las respuestas

    Parameters
    ----------
    data : array
        Datos en crudo.

    Returns
    -------
    data_clean : array
        datos limpios.

    """
   
    data = remove_id(data)
        
    data = remove_nan(data)
    
    data_clean = clean_data(data)
    
    return data_clean

#%%

#Likert

def neg_pos(data):
    """
    Separa los datos de las preguntas Likert en negativos y positivos.
    Los datos tienen que estar en el orden estándar, en donde los negativos están en posiciones 1, 3 y 6

    Parameters
    ----------
    data : array
        datos limpios (sin id) con 11 columnas.

    Returns
    -------
    neg : array
        respuestas de preguntas Likert negativas.
    pos : array
        espuestas de preguntas Likert positivas.

    """
    neg = data[:,[1, 3, 6]]
    pos = np.delete(data, [1, 3, 6], axis=1)
    
    return neg, pos
    
#%%

#Violin

def adjacent_values(vals, q1, q3):
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value


def set_axis_style(ax, labels, x_label):
    ax.set_xticks(np.arange(1, len(labels) + 1), rotation=45, labels=labels)
    ax.set_xlim(0.25, len(labels) + 0.75)
    ax.set_xlabel(x_label)

def violin(ax, data, title, labels, x_label="Atributos",
           facecolor='paleturquoise', edgecolor='black',
           med_col='k', med_marker='_', med_s=50,
           q_vline='teal', w_vline='teal'):
    
    ax.set_title(title)
    parts = ax.violinplot(
            data, showmeans=False, showmedians=False,
            showextrema=False)

    for pc in parts['bodies']:
        pc.set_facecolor(facecolor)
        pc.set_edgecolor(edgecolor)
        pc.set_alpha(1)

    quartile1, medians, quartile3 = np.percentile(data, [25, 50, 75], axis=0) #obtengo cuartiles

    whiskers = np.array([adjacent_values(sorted_array, q1, q3)                  
        for sorted_array, q1, q3 in zip(data, quartile1, quartile3)])

    whiskers_min, whiskers_max = whiskers[:, 0], whiskers[:, 1]

    inds = np.arange(1, len(medians) + 1)
    ax.scatter(inds, medians, marker=med_marker, color= med_col, s=med_s, zorder=3)
    ax.vlines(inds, quartile1, quartile3, color=q_vline, linestyle='-', lw=4)
    ax.vlines(inds, whiskers_min, whiskers_max, color=w_vline, linestyle='-', lw=2)

    ax.yaxis.grid(True)

    set_axis_style(ax, labels, x_label)

    ax.set_yticks(np.arange((np.min(data)-1), (np.max(data)+1)))

def graph_neg_pos(data, labels,
                  title1="Preguntas positivas", title2="Preguntas negativas",
                  ylabel='Escala likert (1-5)', x_label="Atributos",
                  facecolor='paleturquoise', edgecolor='black',
                  med_col='k', med_marker='_', med_s=50,
                  q_vline='teal', w_vline='teal'):
    
    neg_label = [labels[i] for i in [1, 3, 6]]
    pos_label = [labels[i] for i in range(len(labels)) if i not in [1, 3, 6]]
        
    neg, pos = neg_pos(data)  #separo datos en neg y pos
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4), sharey=True)
    
    violin(ax1, pos, title1, pos_label, x_label, facecolor, edgecolor,
           med_col, med_marker, med_s, q_vline, w_vline)
    
    violin(ax2, neg, title2, neg_label, x_label, facecolor, edgecolor,
           med_col, med_marker, med_s, q_vline, w_vline)
    
    ax1.set_ylabel(ylabel)

    plt.show()