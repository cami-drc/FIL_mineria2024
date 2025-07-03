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
    Función para quitar las filas y columnas que tienen PURO nan

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
    Para quitar las filas (respuestas individuales) que no respondieron todas las preguntas.
    Es decir, no toda la columna/fila está llena de nan. NO FUNCIONA CON STRINGS

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
    y las filas (respuestas individuales) que no respondieron todas las preguntas.

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

def edad_clean(data):
    
    arr_float = data.astype(np.float64)

    hay_nan = np.isnan(arr_float).any()

    
    if hay_nan:
        print("Hay valores NaN en la columna")
        data_clean = clean_data(data)
        return data_clean
    else:
        print("No hay valores NaN en la columna")
        return data

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

#Likert

def violin(ax, data, labels, title="Violin plot", palette="colorblind"):
    """
    Función que hace gráficas de violin para la función "graph_neg_pos".

    Parameters
    ----------
    ax : variable
        el ax a usar en la función "graph_neg_pos".
    data : array
        los datos a graficar.
    labels : list/array
        las etiquetas con los atributos.
    title : string, optional
        el título de la gráfica. The default is "Violin plot".
    palette : string, optional
        la paleta de colores a usar en la gráfica. The default is "colorblind".

    Returns
    -------
    None.

    """
    
    sns.violinplot(ax=ax, data=data, palette=palette)

    ax.set_xticks(ticks=range(len(labels)), labels=labels, rotation=45)

    ax.set_title(title)
   
def graph_neg_pos(data, labels,title="Preguntas Likert",
                  title1="Atributos positivas", title2="Atributos negativas",
                  ylabel='Escala Likert (1-5)', palette="colorblind",
                  text=True, espanol=True):
    """
    Hace una figura donde están separados los resultados de las preguntas Likert
    positivas y negativas.

    Parameters
    ----------
    data : array
        los datos a graficar (combinados pos y neg). Tienen que estar en el mismo
        orden que se hicieron las preguntas (no separar pos y neg).
    labels : array/list
        las etiquetas con los atributos (puedes meterlas en inglés o en español).
    title : string, optional
        el título de la figura. The default is "Preguntas Likert".
    title1 : string, optional
        título de la gráfica 1. The default is "Atributos positivas".
    title2 : string, optional
        título de la gráfica 2. The default is "Atributos negativas".
    ylabel : string, optional
        título del eje y. The default is 'Escala Likert (1-5)'.
    palette : string, optional
        paleta de colores a usar. The default is "colorblind".
    text : BOOL, optional
        si es True, se inclluye un pie de figura que menciona la cantidad de respuestas.
        The default is "True".
    espanol : BOOL, optional
        si es True, el pie de figura, el título y el eje y se escriben en español;
        si es False, en inglés.
        The default is "True".

    Returns
    -------
    None.

    """
    
    neg_label = [labels[i] for i in [1, 3, 6]]
    pos_label = [labels[i] for i in range(len(labels)) if i not in [1, 3, 6]]
        
    neg, pos = neg_pos(data)  #separo datos en neg y pos
    
    cont = data[:,0].size

    
    if espanol:
        texto = "Preguntas de escala tipo Likert donde 1 es muy en desacuerdo y 5 es muy de acuerdo. El número de respuestas es " +str(cont)
    else:
        texto = "Likert scale question where 1 es completely disagree, and 5 is completely agree.  The number of responses is " +str(cont)
        ylabel = "Likert Scale (1-5)"
        title1 = "Positive Attributes"
        title2 = "Negative Attributes"
        title = "Likert Scale Questions"
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(9, 4), sharey=True)
    
    fig.suptitle(title, size="xx-large", weight="roman", y=1.0)
    
    plt.subplots_adjust(top=0.8, bottom=0.3)
    
    if text:
        plt.figtext(0.5, 0.02, texto, va="bottom", ha='center', fontsize=9) 
    
    violin(ax1, pos, pos_label, title=title1, palette=palette)
    
    violin(ax2, neg, neg_label, title=title2, palette=palette)

    ax1.set_ylabel(ylabel)

    plt.show()
#%%

#Calif general

def calif (data, title="Calificación general",
           xlabel="Participantes", ylabel="Puntaje calificación (1-10)",
           text=True, espanol=True):
    """
    Grafica la distribución de respuestas a la pregunta de "Calificación general".

    Parameters
    ----------
    data : array
        array con los datos de calificación general.
    title : string, optional
        título de la figura. The default is "Calificación general".
    xlabel : string, optional
        título del eje x. The default is "Participantes".
    title : string, optional
        título del eje y. The default is "Puntaje calificación (1-10)".
    text : BOOL, optional
        si es True, se inclluye un pie de figura que menciona el 
        promedio (redondeado a 2 decimales) y cantidad de respuestas.
        The default is "True".
    espanol : BOOL, optional
        si es True, el pie de figura, el título y el eje y se escriben  en español;
        si es False, en inglés.
        The default is "True".

    Returns
    -------
    None.

    """
    
    promedio = np.mean(data)
    prom_red = round(promedio, 2)
    cont = data.size

    if espanol:
        texto = "Calificación general donde 1 es pésimo y 10 es excelente. El número de respuestas es " +str(cont)+ " y el promedio es de " +str(prom_red)
    else:
        texto = "General score where 1 is horrible and 10 is excellent. The number of responses is " +str(cont)+ " and the average is " +str(prom_red)
        xlabel = "Participants"
        ylabel = "Score (1-10)"
        title = "General Score"

    plt.figure(figsize=(10, 6))  # tamaño de figura

    sns.violinplot(data=data) #diagrama de violin 

    plt.ylim(1, 10) #rangos en y 
    plt.axhline(y=promedio, color='red', linestyle='--', label='Promedio') #línea para promedio 
   
    plt.legend(loc="lower right") #leyenda 
    
    plt.subplots_adjust(top=0.9) #espacio adicional entre gráfica y título 
   
    plt.xlabel(xlabel) #eje x título 
    plt.ylabel(ylabel) #eje y título 
    
    if text:
        plt.figtext(0.5, 0.02, texto, ha='center', fontsize=10) 
        # pie de figura, los segundos valores es para moverlo en el eje y y el primero en x para centrarlo o no 
    
    plt.title(title, y=1.05, pad=20, size="xx-large") # para que no slaga pegado a la gráfica el título 
    
    plt.xticks(ticks=[], labels=[xlabel])  # Eliminar las etiquetas del eje x y establecer solo 'Participantes'
    
    plt.show()
#%%

# Edad

def plot_edad(data, title="Distribución de edad",
              xlabel = "Participantes", ylabel = "Edad (años)",
              text = True, espanol = True):
    
    promedio = np.mean(data)
    prom_red = round(promedio, 2)
    cont = data.size

    hline_label = "Promedio"


    if espanol:
        texto = "El número de respuestas es " +str(cont)+ " y el promedio es de " +str(prom_red)
    else:
        texto = "The number of responses is " +str(cont)+ " and the average is " +str(prom_red)
        xlabel = "Participants"
        ylabel = "Age (years)"
        title = "Age Distribution"
        hline_label = "Average"


    sns.violinplot(data=data)


    plt.axhline(y=promedio, color='red', linestyle='--', label=hline_label) #línea para promedio 
    plt.legend(loc="lower right") #leyenda 
                  
    plt.subplots_adjust(top=0.9) #espacio adicional entre gráfica y título 

    plt.xlabel(xlabel) #eje x título 
    plt.ylabel(ylabel) #eje y título 
        
    if text:
        plt.text(0.5, 0.9, '', transform=plt.gca().transAxes)
        plt.figtext(0.5, 0.02, texto, ha='center', fontsize=9) 
        # pie de figura, los segundos valores es para moverlo en el eje y y el primero en x para centrarlo o no 
        
    plt.title(title, y=1.05, pad=20, size="xx-large") # para que no slaga pegado a la gráfica el título 
        
    plt.xticks(ticks=[], labels=[xlabel])  # Eliminar las etiquetas del eje x y establecer solo 'Participantes'
        
    plt.show()
    
#%%

#Género

def autopct_format(conteos):
    """
    Función para hacer las etiquetas dentro del diagrama de pie de "Género".

    Parameters
    ----------
    conteos : array
        cuántas respuestas hay para cada variable (fem/masc).

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    
    def my_format(pct):
        total = sum(conteos)
        val = int(round(pct*total/100.0))
        return f'{pct:.1f}%\n({val:d})'
   
    return my_format


def plot_genero(data, title="Distribución de género",
                   color=['teal', 'steelblue', "gainsboro"],
                   text=True, espanol=True):
    
    valores_unicos, conteos = np.unique(data, return_counts=True)

    cont = np.sum(conteos)
    
    if espanol:
        texto = "El número de respuestas es " +str(cont)
    else:
        texto = "The number of responses is " +str(cont)
        title = "Gender Distribution"
        valores_unicos = np.array(["Women", "Men"])

    plt.figure(figsize=(8, 6))
    plt.pie(conteos, labels=valores_unicos, autopct=autopct_format(conteos),
            startangle=90, colors=color)

    if text:
        plt.text(0.5, 0.9, '', transform=plt.gca().transAxes)
        plt.figtext(0.5, 0.12, texto, ha='center', fontsize=9) 
        # pie de figura, los segundos valores es para moverlo en el eje y y el primero en x para centrarlo o no 
    

    plt.title(title, y=0.92, pad=20, size="xx-large")

    plt.show()

