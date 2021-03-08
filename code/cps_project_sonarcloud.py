#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as mp


# In[78]:


#URL used
URL_NAZIONALE = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-andamento-nazionale.json"
URL_REGIONALE = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
URL_REGIONALE_LATEST = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni-latest.json"

#parameters for the graphs
x_label = "giorni dal 24/02"
y_label = r"$\frac{nuovi\ positivi}{nuovi\ tamponi}$"  
grid_color = "grey"
label_color = "white"
plot_color="green"
title_fontsize = 30
axes_fontsize = 20
text_pad = 20
context = {'axes.edgecolor':'grey', 'axes.facecolor':'black',
           'font.family':'sans-serif', 'figure.facecolor':'black', 'figure.edgecolor':'black',
           'xtick.color':'white', 'ytick.color':'white', 'savefig.transparent':'True'}


# In[79]:


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


# In[80]:


'''
La funzione crea un dataframe sull'andamento giornaliero delle regioni italiane.
L'osservabile scelta è quella dei "nuovi_positivi". Il processo termina
con il garifco a bolle, prodotto dalla funzione "showBubbleGraph()".
'''
def bubbleGraph():
    
    #load data
    data = pd.read_json(URL_REGIONALE_LATEST)

    #filter the dataframe
    dataframe = data.loc[:,['long', 'lat', 'nuovi_positivi']]

    #print and display the dataframe
    print(dataframe)
    showBubbleGraph(dataframe.loc[:,'long'], dataframe.loc[:,'lat'], dataframe.loc[:,'nuovi_positivi'])


# In[81]:


'''
La funzione produce un grafico a linea, prendendo in input i valori
per l'ascissa e l'ordinata, con le relative label.
'''
def showGraph(title, x_axis, first_y_axis, second_y_axis, x_label, y_label, firsti_info_legend, second_info_legend):
    
    with mp.rc_context(context):
  
        mp.figure(figsize=(21,9))
        
        mp.plot(range(0,x_axis), first_y_axis, color=plot_color, label=firsti_info_legend)
        if(not second_y_axis.empty): mp.plot(range(0,x_axis), second_y_axis, color='blue', label=second_info_legend)
        
        mp.title(title, color=label_color, pad=text_pad, fontsize=title_fontsize)
        mp.grid(color=grid_color)

        mp.ylabel(y_label, color=label_color, fontsize=axes_fontsize, labelpad=text_pad)
        mp.xlabel(x_label, color=label_color, fontsize=axes_fontsize, labelpad=text_pad)

        #mp.savefig('graph_new_cases.png')
        legend = mp.legend(fontsize=text_pad)
        mp.setp(legend.get_texts(), color=label_color)
        
        mp.show()        


# In[82]:


'''
La funzione ritorna l'array contenente i nuovi tamponi.
Ogni valore è calcolato sottraendo i temponi del giorno i+1-esimo
a quelli del giorno i-esimo, per il primo giorno questo calcolo non avviene.
In input riceve il dataframe e la sua lunghezza.
'''
def calculateNewSwabs(dataframe, len_dataframe):
    
    new_swabs = []
    
    for i in range(0, len_dataframe):
        if(i == 0): 
            previus_value = dataframe.tamponi[i]
            new_swabs.append(dataframe.tamponi[i])
        else: 
            difference = dataframe.tamponi[i] - previus_value
            previus_value = dataframe.tamponi[i]
            new_swabs.append(difference)

    return new_swabs

'''
La funzione ritorna il rapporto tra "nuovi_positivi/nuovi_tamponi".
In input si hanno: il dataframe, la sua lunghezza e i nuovi tamponi
precedentemente calcolati.
'''
def calculateRatio(dataframe, len_dataframe, new_swabs):
    
    ratio = []
    
    for i in range(0, len_dataframe):
        if new_swabs[i] == 0: ratio.append(0)
        else:
            
            #approximate the number
            approx = round(dataframe.nuovi_positivi[i]/new_swabs[i], 2)
            ratio.append(approx)
            
    return ratio


# In[83]:


'''
La funzione crea un dataframe sull'andamento nazionale italiano, contenente il
rapporto "nuovi_positivi" e "nuovi_tamponi". Il grafico è prodotto da "showGraph()".
Nota: il picco vicino il valore 300 è in corrispondenza della fine di dicembre,
in particolare il 26-27-28-29.
'''
def nationalTrend():

    #load the data
    data = pd.read_json(URL_NAZIONALE)
    
    #pick only "nuovi_positivi" e "tamponi"
    dataframe = data.loc[:,['nuovi_positivi', 'tamponi']]
    
    len_dataframe = len(dataframe)
    #calculate "nuovi_tamponi"
    new_swabs = calculateNewTamponi(dataframe, len_dataframe)

    #calculate the ratio "nuovi_positivi/nuovi_tamponi"
    ratio = calculateRatio(dataframe, len_dataframe, new_swabs)
    
    #add the ratio and new swabs columns
    dataframe["rapporto"] = ratio
    dataframe["nuovi_tamponi"] = new_swabs
        
    #print and display the dataframe 
    print(dataframe)
    showGraph("Andamento nazionale", len_dataframe, dataframe.loc[:,'rapporto'], pd.Series(dtype='float64'), x_label, y_label, "Italia", "null")


# In[84]:


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
    
    #filter the dataframe 
    region_dataframe = data.loc[data.denominazione_regione == region,['nuovi_positivi', 'tamponi']]
    
    #change the index value
    region_dataframe.index = [x for x in range(0, len(region_dataframe.values))]
    len_dataframe = len(region_dataframe)
    
    #calculate the new swabs
    new_swabs_region = calculateNewTamponi(region_dataframe, len_dataframe)
    
    #calculate (nuovi_positivi/nuovi_tamponi)
    region_ratio = calculateRatio(region_dataframe, len_dataframe, new_swabs_region)
    
    #add the ratio and new swabs columns
    region_dataframe["rapporto"] = region_ratio
    region_dataframe["nuovi_tamponi"] = new_swabs_region
    
    print(region_dataframe)
    return region_dataframe

    


# In[85]:


'''
La funzione calcola e mostra, per ogni data dell'andamento regionale, il rapporto
tra "nuovi_positivi" e "nuovi_tamponi". Ciò è svolto in "calculateNewDataframe()".
In aggiunta viene prodotto un grafico di confronto tra le due regioni
scelte dall'utente.
'''
def regionalTrend():
    
    #load the data
    data = pd.read_json(URL_REGIONALE)
    
    #get the first region from the user
    print("Insert a region (e.g. Lazio)")
    input_region_first = inputRegion()
    
    #get the second region from the user
    print("Insert the second region (e.g. Basilicata)\n(Digit null if you don't want)")
    input_region_second = inputRegion()
    
    #filter and calculate a new dataframe with columns: 
    #nuovi_tamponi; rapporto; nuovi_positivi; tamponi
    dataframe_region_first = calculateNewDataframe(data, input_region_first)

    #do the same with the second region
    #if inserted above
    if(input_region_second != "null"): dataframe_region_second = calculateNewDataframe(data, input_region_second)
    else:

        dataframe_region_second = data.loc[data.denominazione_regione == input_region_second,[]]
        dataframe_region_second["rapporto"] = []

    #display the graph
    showGraph("Andamento regionale", len(dataframe_region_first), dataframe_region_first.loc[:,'rapporto'], dataframe_region_second.loc[:,'rapporto'], x_label, y_label, input_region_first, input_region_second)


# In[86]:


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


# In[87]:


'''
La funzione calcola e mostra la media mobile per un certo intervallo di tempo,
in questo caso sette giorni.
'''
def nationalMean():
    
    #load the data
    data = pd.read_json(URL_NAZIONALE)
    
    #pick only "nuovi_positivi" and "data"
    dataframe = data.loc[:,['nuovi_positivi', 'data']]
    len_dataframe = len(dataframe)
    interval_time = 7
    
    #select only the last "interval_time" rows
    dataframe = dataframe.iloc[len_dataframe - interval_time:len_dataframe]

    #select only the column of "nuovi_positivi"
    #and calculate the mean
    mean = (dataframe.loc[:,'nuovi_positivi']).mean()        
    
    #pick only day and month from field "data"
    data_new = []
    for i in range(len_dataframe - interval_time, len_dataframe):
        
        day_month = dataframe.data[i]
        data_new.append(day_month[5:10])
        
    #overload the field "data" with data_new
    dataframe["data"] = data_new
    
    #display and print the dataframe
    print(dataframe)
    showMeanGraph(dataframe.loc[:,'data'], dataframe.loc[:,'nuovi_positivi'], mean, interval_time)


# In[89]:


bubbleGraph()
nationalTrend()
regionalTrend()
nationalMean()


# In[ ]:




