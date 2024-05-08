#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 13:54:51 2024

@author: camiladelrio
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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


def violin(ax, data, labels, title="Violin plot", palette="colorblind"):
    
    sns.violinplot(ax=ax, data=data, palette=palette)

    ax.set_xticks(ticks=range(len(labels)), labels=labels, rotation=45)

    ax.set_title(title)
   

def graph_neg_pos(data, labels,title="Preguntas Likert",
                  title1="Atributos positivas", title2="Atributos negativas",
                  ylabel='Escala likert (1-5)', palette="colorblind"):
    
    neg_label = [labels[i] for i in [1, 3, 6]]
    pos_label = [labels[i] for i in range(len(labels)) if i not in [1, 3, 6]]
        
    neg, pos = neg_pos(data)  #separo datos en neg y pos
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4), sharey=True)
    
    fig.suptitle(title, size="xx-large", weight="roman")

    violin(ax1, pos, pos_label, title=title1, palette=palette)
    
    violin(ax2, neg, neg_label, title=title2, palette=palette)

    ax1.set_ylabel(ylabel)

    plt.show()