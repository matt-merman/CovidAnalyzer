#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import numpy as np
import requests as rq
import json as js
from matplotlib import pyplot as mp


# In[21]:


#URL used
URL_NAZIONALE = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
URL_REGIONALE = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
URL_REGIONALE_LATEST = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json"

#parameters for graphs
grid_color = "grey"
label_color = "white"
plot_color="green"
title_fontsize = 30
axes_fontsize = 20
text_pad = 20
context = {'axes.edgecolor':'grey', 'axes.facecolor':'black',
           'font.family':'sans-serif', 'figure.facecolor':'black', 'figure.edgecolor':'black',
           'xtick.color':'white', 'ytick.color':'white', 'savefig.transparent':'True',
           'figure.facecolor':'black'}


# In[14]:


'''
La funzione stampa un grafico a bolle geocalizzato. A tal fine
prende in input longitudine e latitudine di tutte le regioni, e
un osservabile da graficare, in questo caso ho scelto i "nuovi_positivi"
giornalieri.
'''
def showBubbleGraph(longitudine_array, altitude_array, new_positives_array):
    
    with mp.rc_context(context):

        mp.figure(figsize=(9,10))
        mp.scatter(longitudine_array, altitude_array,  s=new_positives_array, c=new_positives_array, alpha=0.9, cmap='viridis')
        
        mp.grid(color=grid_color)
        
        mp.ylabel("latitudine", color=label_color, fontsize=axes_fontsize, labelpad=text_pad)
        mp.xlabel("longitudine", color=label_color, fontsize=axes_fontsize, labelpad=text_pad)
        mp.title("Nuovi positivi giornalieri", color=label_color, pad=text_pad, fontsize=title_fontsize)
        
        mp.colorbar(label="nuovi positivi")
        
        mp.show()


# In[16]:


'''
La funzione crea un dataframe sull'andamento giornaliero delle regioni italiane.
L'osservabile scelta è quella dei "nuovi_positivi". Il processo termina
con il garifco a bolle, prodotto dalla funzione "showBubbleGraph()".
'''
def function1():
    
    #load data
    data = pd.read_json(URL_REGIONALE_LATEST)
    
    #calculate all value for the regions
    dataframe = data.loc[:,['long', 'lat', 'nuovi_positivi']]

    longitudine_array = []
    altitude_array = []
    new_positives_array = []
    len_dataframe = len(dataframe)
    
    ################
    #da rimuovere cilo, passare direttamente il dataframe
    
    for i in range(0, len_dataframe):
        longitudine_array.append(dataframe.long[i])
        altitude_array.append(dataframe.lat[i])
        new_positives_array.append(dataframe.nuovi_positivi[i])
    
    dataframe["nuovi_positivi"] = new_positives_array
    #show graph
    #showBubbleGraph(longitudine_array, altitude_array, dataframe.loc[:,'nuovi_positivi'])

function1()


# In[4]:


'''
La funzione produce un grafico a linea, prendendo in input i valori
per l'ascissa e l'ordinata, con le relative label.
'''
def showGraph(title, x_axis, y1_axis, y2_axis, x_label, y_label, info_legend1, info_legend2):
    
    #################
    #rifare nomenclatura
    
    with mp.rc_context(context):
  
        mp.figure(figsize=(21,9))
        
        mp.plot(range(0,x_axis), y1_axis, color=plot_color, label=info_legend1)
        if(not y2_axis.empty): mp.plot(range(0,x_axis), y2_axis, color='blue', label=info_legend2)
        
        mp.title(title, color=label_color, pad=text_pad, fontsize=title_fontsize)
        mp.grid(color=grid_color)

        mp.ylabel(y_label, color=label_color, fontsize=axes_fontsize, labelpad=text_pad)
        mp.xlabel(x_label, color=label_color, fontsize=axes_fontsize, labelpad=text_pad)

        #mp.savefig('graph_new_cases.png')
        legend = mp.legend(fontsize=text_pad)
        mp.setp(legend.get_texts(), color=label_color)
        
        mp.show()        


# In[5]:


'''
La funzione ritorna l'array contenente i nuovi tamponi.
Ogni valore è calcolato sottraendo i temponi del giorno i+1-esimo
a quelli del giorno i-esimo, per il primo giorno questo calcolo non avviene.
In input riceve il dataframe e la sua lunghezza.
'''
def calculateNewTamponi(dataframe, len_dataframe):
    
    new_tamponi = []
    
    for i in range(0, len_dataframe):
        if(i == 0): 
            previus_value = dataframe.tamponi[i]
            new_tamponi.append(dataframe.tamponi[i])
        else: 
            nuovi_tamponi = dataframe.tamponi[i] - previus_value
            previus_value = dataframe.tamponi[i]
            new_tamponi.append(nuovi_tamponi)

    return new_tamponi

'''
La funzione ritorna il rapporto tra "nuovi_positivi/nuovi_tamponi".
In input si hanno: il dataframe, la sua lunghezza e i nuovi tamponi
precedentemente calcolati.
'''
def calculateRatio(dataframe, len_dataframe, new_tamponi):
    
    ratio = []
    
    for i in range(0, len_dataframe):
        if new_tamponi[i] == 0:
            ratio.append(0)
        else:
            #approximate the number
            approx = round(dataframe.nuovi_positivi[i]/new_tamponi[i], 2)
            ratio.append(approx)
            
    return ratio


# In[11]:


'''
La funzione crea un dataframe sull'andamento nazionale italiano, contenente il
rapporto "nuovi_positivi" e "nuovi_tamponi". Il grafico è prodotto da "showGraph()".
'''
def function2():

    #load the data
    data = pd.read_json(URL_NAZIONALE)
    
    #pick only "nuovi_positivi" e "tamponi"
    dataframe = data.loc[:,['nuovi_positivi', 'tamponi']]
    #calculate "nuovi_tamponi"
    len_dataframe = len(dataframe)
    new_tamponi = calculateNewTamponi(dataframe, len_dataframe)

    #calculate the rate "nuovi_positivi/nuovi_tamponi"
    ratio = calculateRatio(dataframe, len_dataframe, new_tamponi)
    
    #add the ratio column
    dataframe["rapporto"] = ratio
    dataframe["nuovi_tamponi"] = new_tamponi
    
    print(dataframe)
    
    #display the graph
    x_label = "giorni dal 24/02"
    y_label = r"$\frac{nuovi\ positivi}{nuovi\ tamponi}$"    
    #showGraph("Andamento nazionale", len_dataframe, dataframe.loc[:,'rapporto'], pd.Series(dtype='float64'), x_label, y_label, "Italia", "null")
    
function2()


# In[19]:


'''
La funzione prende in input dall'utente una regione italiana, che ritorna al chiamante.
'''
def inputRegion():
    
    regions = ["Lombardia", "Lazio", "Campania", "Sicilia", "Veneto", "Emilia-Romagna", 
                "Piemonte", "Puglia", "Toscana", "Calabria", "Sardegna", "Liguria", 
                "Marche", "Abruzzo", "Friuli Venezia Giulia", "Umbria", "Basilicata",
                "Molise", "Valle d'Aosta", "P.A. Bolzano", "P.A. Trento", "null"]
    
    input_region = input()    
    while(input_region not in regions): 
        print("Region not valid!\n")
        input_region = input("Insert a region (e.g. Lazio)\n") 
    
    return input_region

'''
La funzione ritorna un dataframe con attributi: "nuovi_positivi", "tamponi",
"rapporto", "nuovi_tamponi". In particolare "rapporto" è quello tra "nuovi_positivi"
e "nuovi_tamponi". 
'''
def calculateNewDataframe(data, region):
    
    #calculate all value for the region 1
    region_dataframe = data.loc[data.denominazione_regione == region,['nuovi_positivi', 'tamponi']]
    
    #change the index value
    region_dataframe.index = [x for x in range(0, len(region_dataframe.values))]
    len_dataframe = len(region_dataframe)
    
    new_tamponi_region = calculateNewTamponi(region_dataframe, len_dataframe)
    
    region_ratio = calculateRatio(region_dataframe, len_dataframe, new_tamponi_region)
    
    #add the ratio column
    region_dataframe["rapporto"] = region_ratio
    region_dataframe["nuovi_tamponi"] = new_tamponi_region
    
    print(region_dataframe)
    return region_dataframe

    


# In[ ]:


'''
La funzione calcola e mostra, per ogni data dell'andamento regionale, il rapporto
tra "nuovi_positivi" e "nuovi_tamponi". Ciò è svolto in "calculateNewDataframe()".
In aggiunta viene prodotto un grafico di confronto tra le due regioni
scelte dall'utente.
'''
def function3():
    
    #load the data
    data = pd.read_json(URL_REGIONALE)
    
    print("Insert a region (e.g. Lazio)\n")
    input_region_first = inputRegion()
    print("Insert the second region (e.g. Basilicata)\n(Digit null if you don't want)\n")
    input_region_second = inputRegion()
    
    dataframe_region_first = calculateNewDataframe(data, input_region_first)

    #calculate all values for the region 2
    if(input_region_second != "null"): dataframe_region_second = calculateNewDataframe(data, input_region_second)
    else:

        dataframe_region_second = data.loc[data.denominazione_regione == input_region_second,[]]
        dataframe_region_second["rapporto"] = []

    #display the graph
    x_label = "giorni dal 24/02"
    y_label = r"$\frac{nuovi\ positivi}{nuovi\ tamponi}$"
    
    showGraph("Andamento regionale", len(dataframe_region_first), dataframe_region_first.loc[:,'rapporto'], dataframe_region_second.loc[:,'rapporto'], x_label, y_label, input_region_first, input_region_second)
    
function3()


# In[9]:


'''
La funzione mostra un grafico a linea e un asintoto orizzonatale per la media
'''
def showMeanGraph(x_axis, y_axis, mean, n):
    
    with mp.rc_context(context):
  
        mp.figure(figsize=(21,9))
        mp.plot(x_axis, y_axis, color=plot_color, label="Italia")
        
        mp.axhline(y=mean, linestyle='dashed', label="media = %d" %(mean))

        mp.title("Media mobile a %d giorni" %(n), color=label_color, pad=text_pad, fontsize=title_fontsize)
        mp.grid(color=grid_color)

        mp.ylabel("nuovi positivi", color=label_color, fontsize=axes_fontsize, labelpad=text_pad)
        mp.xlabel("mese-giorno", color=label_color, fontsize=axes_fontsize, labelpad=text_pad)

        #mp.savefig('graph_new_cases.png')
        legend = mp.legend(fontsize=axes_fontsize)
        mp.setp(legend.get_texts(), color=label_color)
        mp.show()


# In[9]:


'''
La funzione calcola e mostra la media mobile per un certo intervallo di tempo,
in questo caso sette giorni.
'''
def function4():
    
    #load the data
    data = pd.read_json(URL_NAZIONALE)
    
    #pick only "nuovi_positivi"
    dataframe = data.loc[:,['nuovi_positivi', 'data']]
    len_dataframe = len(dataframe)
    interval_time = 7
    
    #select only the last "interval_time" rows
    dataframe = dataframe.iloc[len_dataframe - interval_time:len_dataframe]

    #select only the column of "nuovi_positivi"
    #for the mean()
    latest_new_posites_array = dataframe.loc[:,'nuovi_positivi']
    
    #caluclate the mean()
    #latest_new_posites_array = np.array(latest_new_posites)
    mean = latest_new_posites_array.mean()
        
    #pick only day and month from field "data"
    data_new = []
    for i in range(len_dataframe - interval_time, len_dataframe):
        
        day_month = dataframe.data[i]
        data_new.append(day_month[5:10])
        
    #adding data_new to dataframe
    dataframe["data"] = data_new
    
    showMeanGraph(dataframe.loc[:,'data'], dataframe.loc[:,'nuovi_positivi'], mean, interval_time)
    
function4()


# In[ ]:




