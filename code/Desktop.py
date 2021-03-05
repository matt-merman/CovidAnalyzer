#!/usr/bin/env python
# coding: utf-8

# In[1]:


#site: https://github.com/pcm-dpc/COVID-19
#function 1: grafico a bolle
#function 2: graficare andamento rapporto nuovi_positivi/nuovi_tamponi
#function 3: calcolare andamento regionale nuovi_positivi/nuovi_tamponi
#funciont 4: graficare la media mobile a 7 giorni per andamento nazionale


# In[2]:


#import of all libraries I need
import pandas as pd
import numpy as np
import requests as rq
import json as js
from matplotlib import pyplot as mp


# In[59]:


def showGraph(x_axis, y1_axis, y2_axis, x_label, y_label, info_legend1, info_legend2):
    
    with mp.rc_context({'axes.edgecolor':'black', 'axes.facecolor':'black',
                     'font.family':'sans-serif', 'figure.facecolor':'black', 'figure.edgecolor':'black',
                     'xtick.color':'white', 'ytick.color':'white', 'savefig.transparent':'True',
                     'figure.facecolor':'black'}):
  
        mp.figure(figsize=(21,9))
        mp.plot(range(0,x_axis), y1_axis, color='green', label=info_legend1)
        if(y2_axis != 0): mp.plot(range(0,x_axis), y2_axis, color='blue', label=info_legend2)

        mp.title("Covid trend Italy about %d days" %(x_axis), color="grey", fontsize=20)
        mp.grid(color="grey")

        mp.ylabel(y_label, color="grey", fontsize=20, labelpad=20)
        mp.xlabel(x_label, color="grey", fontsize=20, labelpad=20)

        #mp.savefig('graph_new_cases.png')
        legend = mp.legend(fontsize=20)
        mp.setp(legend.get_texts(), color='w')
        mp.show()        


# In[4]:


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


# In[5]:


#calculate the ratio "nuovi_positivi/nuovi_tamponi"
def calculateRatio(dataset, len_dataframe, new_tamponi):
    
    ratio = []
    
    for i in range(0, len_dataframe):
        if new_tamponi[i] == 0:
            ratio.append(0)
        else:
            #approximate the number
            approx = round(dataset.nuovi_positivi[i]/new_tamponi[i], 2)
            ratio.append(approx)
            
    return ratio


# In[6]:


#function 2
'''
Calcolare e graficare per ogni data dell'andamento nazionale il rapporto
nuovi_positivi e nuovi_tamponi, dove nuove_tamponi è una colonna calcolata
rappresentante il numero di nuovi tampo effettuati
'''
def function2():

    #load the data
    URL = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
    data = pd.read_json(URL)
    
    #pick only "nuovi_positivi" e "tamponi"
    dataframe = data.loc[:,['nuovi_positivi', 'tamponi']]
    #calculate "nuovi_tamponi"
    len_dataframe = len(dataframe)
    new_tamponi = calculateNewTamponi(dataframe, len_dataframe)

    #calculate the rate "nuovi_positivi/nuovi_tamponi"
    ratio = calculateRatio(dataframe, len_dataframe, new_tamponi)
    
    #add the ratio column
    dataframe["Ratio"] = ratio
    dataframe["New tamponi"] = new_tamponi
    print(dataframe)
    
    #display the graph
    x_label = "Days from 24/02"
    y_label = r"$\frac{New\ positives}{New\ tamponi}$"
    #showGraph(len_dataframe, ratio, 0, x_label, y_label, "Italy", "null")
    
function2()


# In[7]:


#function 3
'''
Calcolare per ogni data dell'andamento regionale il rapporto
tra nuovi_positivi e nuovi_tamponi, dove nuovi_tamponi è una colonna calcolata
rappresentante il numero di nuovi tamponi effettuati.
Nota: in aggiunta la funziona produce il grafico della regione, e un grafico di contronto tra due regioni
(se ovvimente viene inserita una seconda regione da confrontare)
'''
def function3():
    
    #load the data
    URL = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
    data = pd.read_json(URL)
    regions = ["Lombardia", "Lazio", "Campania", "Sicilia", "Veneto", "Emilia-Romagna", 
                "Piemonte", "Puglia", "Toscana", "Calabria", "Sardegna", "Liguria", 
                "Marche", "Abruzzo", "Friuli Venezia Giulia", "Umbria", "Basilicata",
                "Molise", "Valle d'Aosta", "P.A. Bolzano", "P.A. Trento", "null"]

    input_region1 = input("Insert a region (e.g. Lazio)\n")    
    while(input_region1 not in regions): 
        print("Region not valid!\n")
        input_region1 = input("Insert a region (e.g. Lazio)\n")    
    
    input_region2 = input("Insert the second region (e.g. Basilicata)\n(Digit null if you don't want)\n")    
    while(input_region2 not in regions): 
        print("Input not valid!\n")        
        input_region2 = input("Insert the second region (e.g. Basilicata)\n(Digit null if you don't want)\n")    
        
    
    #calculate all value for the region 1
    region1_dataframe = data.loc[data.denominazione_regione == input_region1,['nuovi_positivi', 'tamponi']]
    #change the index value
    region1_dataframe.index = [x for x in range(0, len(region1_dataframe.values))]
    len_dataframe = len(region1_dataframe)
    new_tamponi_region1 = calculateNewTamponi(region1_dataframe, len_dataframe)
    region1_ratio = calculateRatio(region1_dataframe, len_dataframe, new_tamponi_region1)
    
    #add the ratio column
    region1_dataframe["Ratio"] = region1_ratio
    region1_dataframe["New tamponi"] = new_tamponi_region1
    print(region1_dataframe)
    
    
    #calculate all value for the region 2
    region2_ratio = 0
    if(input_region2 != "null"): 
        region2_dataframe = data.loc[data.denominazione_regione == input_region2,['nuovi_positivi', 'tamponi']]
        region2_dataframe.index = [x for x in range(0, len(region2_dataframe.values))]
        new_tamponi_region2 = calculateNewTamponi(region2_dataframe, len_dataframe)
        region2_ratio = calculateRatio(region2_dataframe, len_dataframe, new_tamponi_region2)
        
        #add the ratio column
        region2_dataframe["Ratio"] = region2_ratio
        region2_dataframe["New tamponi"] = new_tamponi_region2
        print(region2_dataframe)

    #display the graph
    x_label = "$Days\ from\ 24/02$"
    y_label = r"$\frac{New\ positive}{New\ tamponi}$"
    #showGraph(len_dataframe, region1_ratio, region2_ratio, x_label, y_label, input_region1, input_region2)
    
function3()


# In[49]:


def showBubbleGraph(longitudine_array, altitude_array, new_positives_array):
    
    with mp.rc_context({'axes.edgecolor':'black', 'axes.facecolor':'black',
                     'font.family':'sans-serif', 'figure.facecolor':'black', 'figure.edgecolor':'black',
                     'xtick.color':'white', 'ytick.color':'white', 'savefig.transparent':'True',
                     'figure.facecolor':'black'}):

        mp.figure(figsize=(9,10))
        mp.scatter(longitudine_array, altitude_array,  s=new_positives_array, c=new_positives_array, alpha=0.9, cmap='viridis')
        mp.grid(color="grey")
        mp.ylabel("Latitudine", color="grey", fontsize=15, labelpad=20)
        mp.xlabel("Longitudine", color="grey", fontsize=15, labelpad=20)
        mp.title("Nuovi positivi giornalieri", color="grey", fontsize=20)
        mp.colorbar(label="nuovi positivi")
        mp.show()


# In[64]:


#function1
def function1():
    
    #load data
    URL = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json"
    data = pd.read_json(URL)
    
    #calculate all value for the regions
    dataframe = data.loc[:,['long', 'lat', 'nuovi_positivi']]
    
    longitudine_array = []
    altitude_array = []
    new_positives_array = []
    len_dataframe = len(dataframe)
    
    for i in range(0, len_dataframe - 1):
        longitudine_array.append(dataframe.long[i])
        altitude_array.append(dataframe.lat[i])
        new_positives_array.append(dataframe.nuovi_positivi[i])
    
    #show graph
    #showBubbleGraph(longitudine_array, altitude_array, new_positives_array)

function1()


# In[28]:


def function4():
    
    #load the data
    URL = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
    data = pd.read_json(URL)
    
    #pick only "nuovi_positivi"
    dataframe = data.loc[:,['nuovi_positivi']]
    len_dataframe = len(dataframe)

    #calculate the rate "nuovi_positivi/nuovi_tamponi"
    latest_new_posites = []
    interval_time = 7
    
    for i in range(len_dataframe - interval_time, len_dataframe):
        #approximate the number
        latest_new_posites.append(dataframe.nuovi_positivi[i])
            
    #add the ratio column
    print(latest_new_posites)
    
    #caluclate the mean()
    latest_new_posites_array = np.array(latest_new_posites)
    latest_new_posites_array.mean()
    print(latest_new_posites_array.mean())
    
    #show graph
    #...
    
    
function4()


# In[ ]:




