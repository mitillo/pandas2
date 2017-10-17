# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 16:31:22 2017

@author: jaime
"""
import os 
import re
def creacion_rectangulos():
#    def creasop(valor1,valor2,tamano=0.0001,decimales=4):
#    #    valor1,valor2=1.23454,1.28905
#        listavalores=[valor1,valor2]
#        listavalores=sorted(listavalores)
#        soporte=np.around(np.arange(listavalores[0],listavalores[1],tamano),decimals=decimales)
#
#        return(soporte)
    #%% Obtencion rectangulos

    sop_base=set([1.171662, 1.175568,0.898229, 0.902138])
    directorio='C:\\Users\\jaime\\AppData\\Roaming\\MetaQuotes\\Terminal\\3212703ED955F10C7534BE8497B221F4\\profiles\\1dia'
    archivos=os.listdir(directorio)
    archivos=archivos[:-1]
    #file=open(os.path.join(directorio,archivos[2]),'r')
    
    clavessop=[]
    soportesdivisa=[]
    soportefloat=[]
    dicciosoportes={}
    #%%
    #creacion patrones regex
    rectangulo=re.compile(r"object_name=Rectangle \d+\nperiod_flags=\d\ncreate_time=\d+\ncolor=\d+\nstyle=\d\nweight=\d\nbackground=\d\nfilling=\d\nselectable=\d\nhidden=\d\nzorder=\d\ntime_0=\d+\nvalue_0=\d[.\d]+\ntime_1=\d+\nvalue_1=\d[.\d]+\nray=\d")
    divisa=re.compile(r"\nsymbol=.{3,10}")
    
    soporte1=re.compile(r"\nvalue_\d=\d[.\d]+") # lo uso para una vez tomado lo mayor tomar solo la linea que me interesa
    soportenum=re.compile(r"\d[.\d]+")   # este es el ultimo paso donde cogeria el valor numerico
    
    #%%
    for archivo in archivos:
    #    archivo='chart01.chr'
    #    print(archivo)
    
        with open(os.path.join(directorio,archivo),'r') as plantilla:
            contenidos=plantilla.read()
    #        print(contenidos)
           
            
            buscar=rectangulo.findall(contenidos)  #busco rectangulos
            divi=divisa.findall(contenidos)         #busco la clave de la divisa
            divi=[ value.replace("\nsymbol=","") for value in divi]
            divi=[ str.lower(value) for value in divi]
            divi=[ value.replace("#","") for value in divi]
            divi=[ value.replace("i.","") for value in divi]
            divi=[ value.replace("_z7","") for value in divi]
            divi=divi[0]
#            print(divi)
            if divi.startswith ('bund'):
                divi='bund'
            elif divi.startswith ('ustnote'):
                divi='ustnote'
                
#            print(divi)
    #        print(divi)
            divi=str.lower(divi) + 'd1'
    #        print(divi)
            clavessop.append(divi)
            soportes=[]
            for value in buscar:
#                print(buscar)
                sop=soporte1.findall(value)    #aqui busco el valor el cual contiene str
                for valor in sop:
#                    print(valor)
                    sop2=soportenum.findall(valor)     #en este quito los str de sop usando solo los numeros
                    sop2=sop2[0]                    # como cada valor es una lista estas lineas se encargan de pasarlos a float para post uso
                    sop2=float(sop2)
                    soportes.append(sop2)
                    soportefloat.append(soportes)
                    soportes2=[]
                    soportes=set(soportes)
                    soportes=list(soportes-sop_base)
                    x=0
                    y=2
                    longitud=len(soportes)
                    while y<= longitud:
                    #    for valor in soportes:
                            soportes2.append(sorted(soportes[x:y]))
                            x+=2
                            y+=2
#                    soportes2=soportes2[1:]

#                    print(sop_base[0] in soportes2,sop_base[1] in soportes2)
#                    for value in soportes2:
#                        
#                        for rectan in sop_base:
#                            if rectan in value:
#                                print(rectan in value)
#                                value.remove(rectan)
#                            print(divi)
                    if len(soportes2)!=0:
                        dicciosoportes[divi]=soportes2
    return(dicciosoportes)