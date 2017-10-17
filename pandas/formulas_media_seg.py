# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 18:52:56 2017

@author: jaime
"""
#columna='ma200'
#def distma200(row, columna='ma200'):
#    
#    if row.Close < row.ma200:
#        operacion=(row.High - row[columna])*100000
#        return(operacion)
#        
#    elif row.Close > row.ma200:
#        operacion=(row.Low - row[columna])*100000
#        
#        return(operacion)    
#        
#columnadist='madist200'
#operacionsoporteinside='MED200sop'
#operacionresistenciainside='MED200res'
#operacionacercamientosoporte='AT200sop'
#operacionacercamientoresistencia='AT200res'

#def distmedia200(row,columna=columna,columnadist=columnadist,operacionresistenciainside=operacionresistenciainside,operacionsoporteinside=operacionsoporteinside,
#              operacionacercamientosoporte=operacionacercamientosoporte,operacionacercamientoresistencia=operacionacercamientoresistencia):
#        media=row[columna]
#        media=float(format(media,'.4f'))
#        minimo=float(format(row.Low,'.4f'))
#        cierreanterior=float(format(row.cierreanterior,'.4f'))
#        maximo=float(format(row.High,'.4f'))
##        listaoperacion=[]
#        if media > minimo and media < maximo:  #inside es decir que media esta en rango de vela
#            
#            if media>cierreanterior:
#                operacion=operacionresistenciainside
##                listaoperacion.append(operacion)  
#                return(operacion)
#            else:
#                operacion= operacionsoporteinside
##                listaoperacion.append(operacion)
#                return(operacion)
#        elif row[columnadist] > -500 and row[columnadist] < 0:
#            operacion= operacionacercamientoresistencia
#            return(operacion)
##            listaoperacion.append(operacion)  
#        elif row[columnadist] < 500 and row[columnadist] > 0:
#            operacion= operacionacercamientosoporte
#            return(operacion)
##            listaoperacion.append(operacion)  
        
#        return(operacion)


#def distmedia200(row):
#        media=row['ma200']
#        media=float(format(media,'.4f'))
#        minimo=float(format(row.Low,'.4f'))
#        cierreanterior=float(format(row.cierreanterior,'.4f'))
#        maximo=float(format(row.High,'.4f'))
##        listaoperacion=[]
#        if media > minimo and media < maximo:  #inside es decir que media esta en rango de vela
#            
#            if media>cierreanterior:
#                operacion='MED200res'
##                listaoperacion.append(operacion)  
#                return(operacion)
#            else:
#                operacion= 'MED200sop'
##                listaoperacion.append(operacion)
#                return(operacion)
#        elif row[columnadist] > -500 and row[columnadist] < 0:
#            operacion= 'AT200res'
#            return(operacion)
##            listaoperacion.append(operacion)  
#        elif row[columnadist] < 500 and row[columnadist] > 0:
#            operacion= 'AT200sop'
#            return(operacion)
#
#
#def distmedia100(row):
#        media=row['ma100']
#        media=float(format(media,'.4f'))
#        minimo=float(format(row.Low,'.4f'))
#        cierreanterior=float(format(row.cierreanterior,'.4f'))
#        maximo=float(format(row.High,'.4f'))
##        listaoperacion=[]
#        if media > minimo and media < maximo:  #inside es decir que media esta en rango de vela
#            
#            if media>cierreanterior:
#                operacion='MED100res'
##                listaoperacion.append(operacion)  
#                return(operacion)
#            else:
#                operacion= 'MED100sop'
##                listaoperacion.append(operacion)
#                return(operacion)
#        elif row[columnadist] > -500 and row[columnadist] < 0:
#            operacion= 'AT100res'
#            return(operacion)
##            listaoperacion.append(operacion)  
#        elif row[columnadist] < 500 and row[columnadist] > 0:
#            operacion= 'AT100sop'
#            return(operacion)
#
#def distmedia50(row):
#        media=row['ma50']
#        media=float(format(media,'.4f'))
#        minimo=float(format(row.Low,'.4f'))
#        cierreanterior=float(format(row.cierreanterior,'.4f'))
#        maximo=float(format(row.High,'.4f'))
##        listaoperacion=[]
#        if media > minimo and media < maximo:  #inside es decir que media esta en rango de vela
#            
#            if media>cierreanterior:
#                operacion='MED50res'
##                listaoperacion.append(operacion)  
#                return(operacion)
#            else:
#                operacion= 'MED50sop'
##                listaoperacion.append(operacion)
#                return(operacion)
#        elif row[columnadist] > -500 and row[columnadist] < 0:
#            operacion= 'AT50res'
#            return(operacion)
##            listaoperacion.append(operacion)  
#        elif row[columnadist] < 500 and row[columnadist] > 0:
#            operacion= 'AT50sop'
#            return(operacion)






def distma200(row):
    
        if row.Close < row['ma200']:
            operacion=(row.High - row['ma200'])*100000
            return(operacion)
            
        elif row.Close > row['ma200']:
            operacion=(row.Low - row['ma200'])*100000
            
            return(operacion)    



def distmedia200(row):
        media=row['ma200']
        media=float(format(media,'.4f'))
        minimo=float(format(row.Low,'.4f'))
        cierreanterior=float(format(row.cierreanterior,'.4f'))
        maximo=float(format(row.High,'.4f'))
#        listaoperacion=[]
        if media > minimo and media < maximo:  #inside es decir que media esta en rango de vela
            
            if media>cierreanterior:
                operacion='MED200res'
#                listaoperacion.append(operacion)  
                return(operacion)
            else:
                operacion= 'MED200sop'
#                listaoperacion.append(operacion)
                return(operacion)
        elif row['madist200'] > -500 and row['madist200'] < 0:
            operacion= 'AT200res'
            return(operacion)
#            listaoperacion.append(operacion)  
        elif row['madist200'] < 500 and row['madist200'] > 0:
            operacion= 'AT200sop'
            return(operacion)




def distma100(row):

    if row.Close < row['ma100']:
        operacion=(row.High - row['ma100'])*100000
        return(operacion)
        
    elif row.Close > row['ma100']:
        operacion=(row.Low - row['ma100'])*100000
        
        return(operacion)    
        return(operacion)    
        
def distmedia100(row):
        media=row['ma100']
        media=float(format(media,'.4f'))
        minimo=float(format(row.Low,'.4f'))
        cierreanterior=float(format(row.cierreanterior,'.4f'))
        maximo=float(format(row.High,'.4f'))
#        listaoperacion=[]
        if media > minimo and media < maximo:  #inside es decir que media esta en rango de vela
            
            if media>cierreanterior:
                operacion='MED100res'
#                listaoperacion.append(operacion)  
                return(operacion)
            else:
                operacion= 'MED100sop'
#                listaoperacion.append(operacion)
                return(operacion)
        elif row['madist100'] > -500 and row['madist100'] < 0:
            operacion= 'AT100res'
            return(operacion)
#            listaoperacion.append(operacion)  
        elif row['madist100'] < 500 and row['madist100'] > 0:
            operacion= 'AT100sop'
            return(operacion)
#


def distma50(row):

    if row.Close < row['ma50']:
        operacion=(row.High - row['ma50'])*100000
        return(operacion)
        
    elif row.Close > row['ma50']:
        operacion=(row.Low - row['ma50'])*100000 
        return(operacion)
def distmedia50(row):
        media=row['ma50']
        media=float(format(media,'.4f'))
        minimo=float(format(row.Low,'.4f'))
        cierreanterior=float(format(row.cierreanterior,'.4f'))
        maximo=float(format(row.High,'.4f'))
#        listaoperacion=[]
        if media > minimo and media < maximo:  #inside es decir que media esta en rango de vela
            
            if media>cierreanterior:
                operacion='MED50res'
#                listaoperacion.append(operacion)  
                return(operacion)
            else:
                operacion= 'MED50sop'
#                listaoperacion.append(operacion)
                return(operacion)
        elif row['madist50'] > -500 and row['madist50'] < 0:
            operacion= 'AT50res'
            return(operacion)
#            listaoperacion.append(operacion)  
        elif row['madist50'] < 500 and row['madist50'] > 0:
            operacion= 'AT50sop'
            return(operacion)









