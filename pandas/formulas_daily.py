# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 20:58:39 2017

@author: jaime
"""
import pandas as pd
import pickle
import copy
import matplotlib.pyplot as plt
import sopres_rectangulo_new as sopre
import seaborn as sns
import formulas_media_seg as med_seg
import numpy as np
import re
import os
from functools import reduce
import glob
from decimal import ROUND_DOWN,ROUND_UP,Decimal

claves_indices=pickle.load(open('claves_indices.tkl','rb'))

dicciosoportes=sopre.creacion_rectangulos()  
def Tablas2 (route,usofiltro=True,filtro=True,saltar=0,filtrofecha='2016-09',filtroiloc=-50,sustcsv='1440.csv',sustdia='d1'):   
   
    
    Mitabla=pd.read_csv( route ,names=["Date","Time","Open","High","Low","Close",
                                                                       "Vol"],
    
    header=0,usecols=[0,1,2,3,4,5,6],index_col=0,
    parse_dates=True,
    infer_datetime_format=True,
    dayfirst=True,skiprows=saltar)
    if usofiltro==True:
        if filtro==True:
            Mitabla=Mitabla.loc[filtrofecha:]
        else:
            Mitabla=Mitabla.iloc[filtroiloc:]
       
    Mitabla=Mitabla.assign(Rango=Mitabla["High"]-Mitabla["Low"])
    Mitabla=Mitabla.assign(percambio=(Mitabla['Close'].pct_change())*100)
    ex=Mitabla.loc['2017':].expanding()
    rol=Mitabla.loc['2017':].rolling(window=20)
    rol7=Mitabla.rolling(window=5)
    rol60=Mitabla.loc['2017':].rolling(window=60)
    rolmaxmin=Mitabla.rolling(window=2)
    std=rol['Vol'].std()
    Mitabla['ma50']=Mitabla['Close'].rolling(window=50).mean()
    Mitabla['ma100']=Mitabla['Close'].rolling(window=100).mean()
    Mitabla['ma200']=Mitabla['Close'].rolling(window=200).mean()
    Mitabla['cierreanterior']=Mitabla['Close'].shift(3)
    Mitabla['cierreanterior2']=Mitabla['Close'].shift(1)
    Mitabla['rango']=Mitabla['High']- Mitabla['Low']
    

            
#%% Con este apartado lo que quiero es trabajar las medias tener en cuenta siempre poner columna encima de la media que quiero calcular ya que es un kwarg que lo tengo en form que esta en otro archivo

    try:    
    
        Mitabla['madist200']=Mitabla.apply(med_seg.distma200,axis=1)
        Mitabla['sopres200']=Mitabla.apply(med_seg.distmedia200,axis=1)
    
    


        Mitabla['madist50']=Mitabla.apply(med_seg.distma50,axis=1)
        Mitabla['sopres50']=Mitabla.apply(med_seg.distmedia50,axis=1)
        Mitabla['highdif']=(Mitabla['High']-Mitabla['ma50'])*100000
        Mitabla['lowdif']=(Mitabla['Low']-Mitabla['ma50'])*100000
    
    

        
        Mitabla['madist100']=Mitabla.apply(med_seg.distma100,axis=1)
        Mitabla['sopres100']=Mitabla.apply(med_seg.distmedia100,axis=1)
        Mitabla['union']=Mitabla[['sopres200','sopres100','sopres50']].values.tolist()
#        Mitabla['union2']= Mitabla[['sopres200','sopres100', 'sopres50']] 
    except:
       pass
    
  
      
    meanrango=rol['Rango'].mean()
    stdrango=(rol['Rango'].std())*100000
    Mitabla['meanrango']=(meanrango)*100000
    Mitabla['stdrango']=Mitabla['meanrango']+stdrango
    
    Mitabla['Volmean']=round(Mitabla['Vol'].rolling(window=20).mean(),0)
    Mitabla['Volchange']=round(Mitabla['Vol'].pct_change()*100,0)
    try:
        Mitabla['Volstd']=Mitabla['Volmean']+std
        Mitabla['Volstd2']=Mitabla['Volmean']+(2*std)
        Mitabla['Volstd3']=Mitabla['Volmean']+(3*std)
#        
        Mitabla['Volstdneg']=Mitabla['Volmean']-std
        Mitabla['Volstd2neg']=Mitabla['Volmean']-(2*std)
        Mitabla['Volstd3neg']=Mitabla['Volmean']-(3*std)
#        print(Mitabla['Volstd2'])
#        print(Mitabla['Volstd3'])
    except:
        pass
#    Mitabla['Volmeanchange']=round(Mitabla['Volmean']/Mitabla['Vol'],0)
    Mitabla['cumyear']=round(ex['percambio'].aggregate(np.sum),3)
    Mitabla['cum60']=round(rol60['percambio'].sum(),3)
    Mitabla['cum20']=round(rol['percambio'].sum(),3)
    Mitabla['cum7']=round(rol7['percambio'].sum(),3)


    Mitabla.fillna(value=0,inplace=True)
    Mitabla['min']=Mitabla['Low'].rolling(window=2).min()
    Mitabla['max']=Mitabla['High'].rolling(window=2).max()

    Mitabla['min3']=rolmaxmin['Low'].max()
    Mitabla['max3']=rolmaxmin['High'].min()
    
    Mitabla[['max3','min3']]=Mitabla[['max3','min3']].fillna(method='bfill')

   
    return (Mitabla)


#%%La defino aqui para poder utilizarla mas abajo en listacambios y no tener que volver a definirla
listaprueba=pickle.load(open('listaprueba.tkl','rb'))
def operaciones(row):
        if row['percambio'] >0 and row['cum7'] >0 and row['cum20'] >0 :
          operacion='compra'
          return(operacion)
    
        elif row['percambio'] <0 and row['cum7'] <0 and row['cum20'] <0 :
          operacion='venta'
          return(operacion)
      
        elif row['percambio'] >0 and row['cum7'] <0 and row['cum20'] <0 :
          operacion='retr en bajada contraten'
          return(operacion)
      
        elif row['percambio'] <0 and row['cum7'] >0 and row['cum20'] >0 :
          operacion='retr en subida contraten'
          return(operacion)
        else:
            operacion='N'
            return(operacion)




def Analisisdiscreto(activo):
#    activo=EURUSDd1
#    activorango=str.lower(activo[:-2])
#    activo=dic_indices['DAX30']
#    activo=dic_indices['AEX25']
    peurusdd1=copy.deepcopy(activo)

#    print(peurusdd1)
    def rango (row):
        if row['High']>row['max3'] and row['colaventa']>= row ['cuerpo']:
            operacion='inverted'
            return(operacion)
    
#    EURUSDd1['ranges']=EURUSDd1.iloc[-60:].apply(rango,axis=1)
#EURUSDd1.tail(3)

#    peurusdbase=copy.deepcopy(activo)

    
    
    def colasventa(row):
            try:
    #            if row['Rango']<=5:
    #                row['Rango']==10
                if row['Close'] > row['Open']:
                    operacion=(row['High']-row['Close'])
                    operacion=round(operacion/row['Rango']*100,2)
                else:
                    operacion=(row['High']-row['Open'])  
                    operacion=round(operacion/row['Rango']*100,2)             
            except ZeroDivisionError:
                    print('division por cero')
                    operacion=1
            return(operacion)

    def colascompra(row):
#            if row['Rango']<=5:
#                row['Rango']==10
        if row['Close'] > row['Open']:
            operacion=(row['Open']-row['Low'])
            operacion=round((operacion/row['Rango'])*100,2)
        else:
            operacion=(row['Close']-row['Low'])
            operacion=round((operacion/row['Rango']*100),2)
        return(operacion)
#    print(' linea 394 analisis discreto')
    def tipovol(row):
#        #Me llama la atencion como me deja utilizar los 2 return y con ello no me da error de operacion defined before assignment
            if row['Vol'] > row['Volstd3']:
                operacion='Vol > Volstd333'
                return(operacion)
            
            elif row['Vol'] > row['Volstd2']:
                operacion='Vol > Volstd22'
                return(operacion)
            
            elif row['Vol'] > row['Volstd']:
                operacion='Vol > Volstd1'
                return(operacion)
            
            elif row['Vol'] > row['Volmean']:
                operacion='Vol > media'
                return(operacion)
                
            elif row['Vol'] < row['Volstd3neg']:
                operacion='negat > Volstd333'
                return(operacion)
            
            elif row['Vol'] < row['Volstd2neg']:
                operacion='negat > Volstd22'
                return(operacion)
            
            elif row['Vol'] < row['Volstdneg']:
                operacion='negat > Volstd1'
                return(operacion)
            
            else:
                operacion='N'
                return(operacion)
    

        
    peurusdd1['colaventa']=peurusdd1.apply(colasventa, axis=1)
    peurusdd1['colacompra']=peurusdd1.apply(colascompra, axis=1)
    peurusdd1['cuerpo']=abs(round(((peurusdd1['Close']-peurusdd1['Open'])/peurusdd1['Rango'])*100,2))
    
    
    
    def tiporango(row):
#        minimo2=row['low'].iloc[-1]
        if ((row['Low']<row['min3']) and (row['colacompra'] >= row ['cuerpo']) and (row['colacompra'] > row['colaventa'])):
            operacion='martillo'
           
        elif row['High']>row['max3'] and row['colaventa']>= row['cuerpo'] and row['colaventa'] > row['colacompra']:
            operacion='inverted hammer'
#            
        elif row['High']>=row['max3'] and row['colacompra']> row['colaventa'] and row ['cuerpo']< row ['colacompra']:
            operacion= 'hanging man'
#        
#        
        elif row['High']<row['max'] and row['Low']>row['min']:
            operacion='insidebar'
            
        elif row['Close'] > row['Open']:
            operacion='pos'
        else:
            operacion='neg'
        return(operacion)
    
    def unionrange(row):
        operacion=str(np.array([row['colaventa'],row['colacompra'],row['cuerpo']]))
        return(operacion)
       
    
    
    
    
    peurusdd1['vencompcuer']=peurusdd1.apply(unionrange, axis=1)
    peurusdd1['tiporango']=peurusdd1.apply(tiporango, axis=1)
    peurusdd1['tipovol']=peurusdd1.apply(tipovol,axis=1)
    #peurusdd1
#    peurusdd1=peurusdd1.drop(['Rango'], axis=1)
    #peurusdd1.iloc[-3]
#        peurusdd1
    
    def tipovela(row):
        if row['colacompra']>=60:
            operacion='velonCompra'
        
        elif row['colaventa']>=60:
            operacion='velonVenta'
        
        elif row['cuerpo']>= 60:
            operacion='Velon'
        
        else:
            operacion='nada'
        return (operacion)
    
#    def martillo(row):
#        if row['Low']<minimo and row['colaventa']>= 50 and row ['cuerpo']<=50:
#            operacion='martillo'
#        return(operacion)
        
#        elif row['High']>maximo and row['colacompra']>= 50 and row ['cuerpo']<=50:
#                operacion= 'darkstar'
 
    peurusdd1['tipovela']=peurusdd1.apply(tipovela,axis=1)
#    peurusdd1['tipovela']=peurusdd1.apply(martillo,axis=1)
    peurusdd1['Rango']=peurusdd1['Rango']*100000    
    
    def rangetype(row):
        try:
            if row['Rango'] > row['stdrango']:
                operacion='Rango>std'
                return(operacion)
            
            elif row['Rango'] > row['meanrango']:
                operacion='Rango>mean'
                return(operacion)
        except:
            pass      

#%%
    ''' en soportres estar muy atento ya que me dio fallo en indices y me costo idenfificarlos:
        Vamos a utilizar como ejemplo el DAX 
        para evitar esto lo qeu tengo que hacer es
        1º identificar indices (es decir donde se encuentra el punto decimal)
        indice=5 esto queiere decir que tengo una parte real con 4 numeros tipo 12455., 13454.
        2º una vez identificado ver donde queiro redondear para obtener soportes y resistemncias.
        en este caso, me interesa verlo en las centenas siendo:
            sop:12400       res: 12500
        3ºdividir por numero donde quiero redondear:
            en este caso pues sería una division por mil para que me de como 1º decimal la cifra donde quiero redondear y buscar sop y res y posteriormente
            los multiplico por 1000 para obtener valor en las mismas unidades que el indice real:
                12455/1000=12.455          sop= 12.4*1000          res= 12.5*1000
        4º Una vez hecho esto los valores pasan a las siguientes funciones. obteniendo sop res etc.'''
        
    def soportesres000(row):
    #    dicsop000={}
#            row=peurusdd1.iloc[-2]
            red=str(row['cierreanterior2'])
            indice=red.index('.')
            minactual=row[['Open','High','Low','Close']].min()
            maxactual=row[['Open','High','Low','Close']].max()
    #        maxactual=peurusdd1.iloc[-1,[1,2,3,4]].max()
        #    print(cierreactual,red)
            if indice==5:
                red2=float(red)
                red2=float(format(red2,'.0f'))
                red2=red2/1000
                sop=float(Decimal(red2).quantize(Decimal('.0'), rounding= ROUND_DOWN))*1000
                res=float(Decimal(red2).quantize(Decimal('.0'), rounding= ROUND_UP))*1000
#                red2=float
            if indice==4:
                numdecimales='00.'
                red2=str(row['cierreanterior2']/10)
                sop=float(Decimal(red2).quantize(Decimal('0.'), rounding= ROUND_DOWN))*10
                res=float(Decimal(red2).quantize(Decimal('0.'), rounding= ROUND_UP))*10
                
            if indice==1:
                numdecimales='.01'
                sop=float(Decimal(red).quantize(Decimal(numdecimales), rounding= ROUND_DOWN))
                res=float(Decimal(red).quantize(Decimal(numdecimales), rounding= ROUND_UP))
        #        print( 'indice = ', indice, key)
            elif indice in np.arange(2,4,1):
                numdecimales='0.'
        #        print( 'indice = ', indice, key)
                sop=float(Decimal(red).quantize(Decimal(numdecimales), rounding= ROUND_DOWN))
                res=float(Decimal(red).quantize(Decimal(numdecimales), rounding= ROUND_UP))
        #    print(key, sop, res,red)
    #        dicsop000[key]=[sop,res]
            
    #            dicsop000[key]=[sop,res]
        #        print( 'indice = ', indice, key)
            
            if minactual < sop:
                minactual2=str(minactual)
                minactual2=minactual2[:6]
                operacion=(' rot sop ', sop, minactual2)
                return(operacion)
            if maxactual > res:
                maxactual2=str(maxactual)
                maxactual2=maxactual2[:6]
                operacion=(' rot resist ' , res, maxactual2)        
                return(operacion)
        

    peurusdd1['soprenew']=peurusdd1.apply(soportesres000,axis=1)
    
    def union2(row):
        listaunion=row['union']
        letraslista=','.join(listaunion)
        letraslista=letraslista.replace('None','')
        return(letraslista)
      
            


#    peurusdd1['letraslista']=peurusdd1.apply(union2,axis=1)




  
    ###############################################################################
    
    
    peurusdd1['operativa']=peurusdd1.apply(operaciones,axis=1)   
    pd.set_option('expand_frame_repr',False)
#    print('linea 599 final de analisis discreto')

    return(peurusdd1)
    
    

                        
                        
                        
listacolumnasd1=['Open', 'High', 'Low', 'Close','percambio','cum7', 'cum20','cum60' , 'cumyear', 'tipovol', 'soprenew','rect','union','tiporango',  'tipovela','operativa']
#listacolanterior=['Open', 'High', 'Low', 'Close',  'sopres', 'sopres32','rect','min' , 'max', 'percambio','cum7', 'cum20','cum60' , 'cumyear',   'vencompcuer',
#                         'tiporango', 'tipovol', 'tipovela','operativa']
def eleccioncols(activo,columnas=listacolumnasd1):

    divisa=copy.deepcopy(activo)

#    print(divisa)
    divisa=divisa[columnas]
    return(divisa)
    
    
    
#diccio=dic_full
#listaclaves=clavesd1
def visioncorrelacion(divisa,diccio,listaclaves,porcentaje_cierre=0.75,porcentaje_cambio=0.6,grafica=False,
                      columna='percambio'):
      
    correla_percambio=[diccio[x][columna] for x in listaclaves]
    correla_percambio=pd.concat(correla_percambio,axis=1,keys=listaclaves,join='inner')
    
    correla_close=[diccio[x]['Close'] for x in listaclaves]
    correla_close=pd.concat(correla_close,axis=1,keys=listaclaves,join='inner')

    correla_percambio=correla_percambio.corr()
    correla_percambio=correla_percambio.round(decimals=3)
    correla_percambio=correla_percambio.loc[divisa]
    correla_percambio=correla_percambio[(correla_percambio<- porcentaje_cambio)|(correla_percambio > porcentaje_cambio)]
    
    correla_close=correla_close.corr()
    correla_close=correla_close.round(decimals=3)
    correla_close=correla_close.loc[divisa]
    correla_close=correla_close[(correla_close<- porcentaje_cierre)|(correla_close > porcentaje_cierre)]
    correladivisa=pd.concat([correla_close,correla_percambio],axis=1,keys=['Cierre',columna])
    correladivisa.sort_values(columna,ascending=False,inplace=True)
    correladivisa['coef_determination']=correladivisa['percambio'].apply(lambda x: round(x**2,3))

#    print(correladivisa)
#    print(len(correladivisa[columna].dropna()))
    if len(correladivisa[columna].dropna())>1:
        if grafica== True:
    #        print(correla_percambio.index,correladivisa.index)
            list_index_divisa=correladivisa.index.tolist()
            df_correladivisa_close=[diccio[x]['Close'] for x in correladivisa.index.tolist()]
            df_correladivisa_close=pd.concat(df_correladivisa_close,keys=list_index_divisa,axis=1,join='inner')
            df_correladivisa_percambio=[diccio[x][columna] for x in correladivisa.index.tolist()]
            df_correladivisa_percambio=pd.concat(df_correladivisa_percambio,keys=list_index_divisa,axis=1,join='inner')
    #        if len(correla_close) > len(correla_percambio):
    #            list_index_close=list(set(correla_close.index)-set(correla_percambio.index))
            list_index_close=list(set(correladivisa.index)-set(correla_percambio.index))
            list_index_percambio=correla_percambio.index.tolist()
            list_index_percambio.remove(divisa)
            print('list index close = ',list_index_close)
            print('list index percambio = ',list_index_percambio)
    #        list_index_close.append(divisa)
    #            list_index_close in list_index_close2
    #            list_index_percambio in list_index_close
    #            list_index_percambio in list_index_divisa
            if len(list_index_percambio)>1:
                print(len(list_index_percambio))
                sns.pairplot(df_correladivisa_percambio,x_vars=list_index_percambio, y_vars= divisa, kind='reg') #percambio
            if len(list_index_close)>1:   
                print(len(list_index_close))
                sns.pairplot(df_correladivisa_close,x_vars=list_index_close, y_vars= divisa, kind='reg')  #cierre
    return(correladivisa)

def full_divisas(dicDivisasd1):
    change=[dicDivisasd1[divisa][['cumyear','cum60','cum20','cum7','percambio']] for divisa in list(dicDivisasd1.keys())]
    dic_cum={}
    for value in ['cumyear','cum60','cum20','cum7','percambio']:
        changedf=pd.concat(change,axis=1,join='inner')
        change_7=changedf[value]
        columnas=list(dicDivisasd1.keys())
        change_7.columns=columnas
        dic_cum[value]=change_7
        dic_cum[value]=dic_cum[value].iloc[-1].sort_values(ascending=False)
    

    for i in range(len(dic_cum['cum7'].index)):
        
        print('%2d)  %-*s  %.3f  \t %2d)  %-*s  %.3f \t %2d)  %-*s  %.3f  \t %2d)  %-*s  %.3f \t %2d)  %-*s  %.3f  ' %(
                                                             i+1,10,dic_cum['cumyear'].index[i],dic_cum['cumyear'][i],
                                                             i+1,10,dic_cum['cum60'].index[i],dic_cum['cum60'][i],
                                                             i+1,10,dic_cum['cum20'].index[i],dic_cum['cum20'][i],
                                                             i+1,10,dic_cum['cum7'].index[i],dic_cum['cum7'][i],
                                                             i+1,10,dic_cum['percambio'].index[i],dic_cum['percambio'][i]))


def dic_full_divisas(dicDivisasd1):
    change=[dicDivisasd1[divisa][['cum7','cum20','cum60','cumyear','percambio']] for divisa in list(dicDivisasd1.keys())]
    dic_cum={}
    for value in ['cum7','cum20','cum60','cumyear','percambio']:
        changedf=pd.concat(change,axis=1,join='inner')
        change_7=changedf[value]
        columnas=list(dicDivisasd1.keys())
        change_7.columns=columnas
        dic_cum[value]=change_7
        dic_cum[value]=dic_cum[value].iloc[-1].sort_values(ascending=False)
    return(dic_cum)





#diccio=dicd1
def boxplot(divisa,diccio,columna,rango=5):
#    diccio=dicDivisasd1
#    divisa='goldd1'
#    columna='percambio'
    grafica=sns.boxplot(diccio[divisa][columna], fliersize=9)
    rango=rango+1
    if divisa not in claves_indices:
        divisa_ayer=diccio[divisa].iloc[:-1]
    else:
        divisa_ayer=diccio[divisa]
    index_ayer=divisa_ayer.index.tolist()[-5:]
    colores=['red','magenta','orange','green','blue']
    index_color=0
    for i in range(1,rango):
#        print(i)
        grafica.axvline(divisa_ayer[columna][-i], color=colores[index_color],label=index_ayer[-i],linewidth=6)
        grafica.axvline(0, color='cyan')
        index_color+=1
    grafica.legend(fontsize= 'xx-large')
    plt.title(columna + ' semanal',fontsize=20)
    plt.tick_params(axis='both', which= 'major', labelsize=20)
#    return(grafica)
#diccio=dicd1
def plot_full(divisa, diccio):
    plt.figure()
    plt.tick_params(axis='both', which= 'major', labelsize=20)
    plt.plot(diccio[divisa].loc['2017':][['cumyear','cum60','cum20']],linewidth=2)
    plt.legend(['cumyear','cum60','cum20'],loc='upper left', fontsize= 'xx-large')
#    plt.axvline(0,color='cyan')
    plt.figure()
    boxplot(divisa,diccio,'percambio')
    plt.figure()
    boxplot(divisa,diccio,'Vol')
    plt.figure()
    boxplot(divisa,diccio,'Rango')
    


def plot_cambios(diccio,divisa):
#    divisa='gbpusdd1'
    columnas=['cumyear','cum60','cum20','cum7','percambio']
#    diccio=dic_cum
    acumulacion=[]
    acumulacion_values=[]
    for columna in columnas:
        list_index=diccio[columna].index.tolist()
        
        indice=list_index.index(divisa)
        acumulacion.append(indice)
        valor_indice=diccio[columna].iloc[indice]
        acumulacion_values.append(valor_indice)
    
    fig,ax1=plt.subplots(1,1)
    ax1.plot(acumulacion_values[:-1])
#    tickers=ax1.get_xticks()
    ax1.set_xticks(np.array(range(len(columnas[:-1]))))
    ax1.set_xticklabels(columnas)
#    tickers=ax1.get_xticks()
    ax1.axhline(0)
    
    plt.title(divisa)
    plt.show()
    
def slope(divisa,diccionario,valor_iloc=-40,columna=['High','Low','Close']):
    y=diccionario[divisa][columna][valor_iloc:].values
    x=np.array(range(len(y)))
#    coefficients=np.polyfit(x,y,1)
#    coefficients
#    plt.plot(x,y)
    lista_coeficientes=[]

    for i in range(y.shape[1]):
        y2=y[:,i]
        coeficientes=np.polyfit(x,y2,1)
        coeficientes=np.round(coeficientes,5).tolist()
        lista_coeficientes.append(coeficientes)
    plt.figure()
    plt.plot(x,y[:,0],label='High',color='red')
    plt.plot(x,y[:,1],label='Low',color='blue')
    plt.plot(x,y[:,2],label='Close',color='green')
    plt.legend(columna, fontsize= 'xx-large')
    plt.tick_params(axis='both', which= 'major', labelsize=22)
    plt.title('{} \n High coeficients: slope= {} \t intecept={}) \n Low_ coeficients: slope= {} \t intecept={} Close_ coeficients: slope= {} \t intecept={}'.format(
              divisa,lista_coeficientes[0][0],lista_coeficientes[0][1],lista_coeficientes[1][0],lista_coeficientes[1][1],lista_coeficientes[2][0],
              lista_coeficientes[2][1]),fontsize=22)
    plt.show()

    
    
#diccio=dicDivisasd1,
#lista_claves=clavesdivisas    
def visiondicdivisas(diccio,lista_claves):   
    for clave in lista_claves:

        print (clave)
        print( diccio[clave].iloc[-30:],'\n')
        
       
        plt.show()
        if len(correla.dropna())>1:
        
        
            print('\n','#####Tabla corr entre divisas####','\n')
            correla=visioncorrelacion (clave,diccio=diccio, listaclaves=lista_claves)
            print(correla)
            print('\n','#####Correlacion divisa########','\n')
            print(correla.loc[clave])
#            posicionescorrela=correla.loc[clave]
            print('####################')
            print('\n','posiciones abiertas','\n')
#            listaoperaciones=[]
#            correla2=correla.index.tolist() de momento lo quito con el fin de ver que hago y como valoro que divisas cojo para ver que pos tengo abiertas
            correla2=correla['percambio'].dropna().index.tolist()
            correla2=set([divisa[:-2] for divisa in correla2]) #esto lo hago para quitarle el 'd1' a la lista, sino lo hago no coinciden las listas


def divisa_position(dic_full,divisa):
#    divisa='eurusdd1'
    divisa_position=[]
    for key,value in dic_cum.items():
        print(key)
        list_position=dic_cum[key].index.tolist()
        indice_position=list_position.index(divisa)
        divisa_position.append(indice_position)
    
    
    
    