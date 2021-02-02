#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Juan Emilio Martinez Manjon
Asignatura: Programacion Tecnica y Cientifica
Profesor: Eugenio Aguirre Molina
Curso: 2020/2021
"""

# agrupar.py

"""
Este fichero agrupa los puntos capturados desde el simulador en clusters.
Para saber cuantos puntos hay en cada cluster usaremos los parámetros
minpuntos, maxpuntos y umbral.

Después de hacer varias pruebas empíricas y analizando los resultados finales
he llegado a la conclusión de que los mejores parámetros para este problema
son:
    
    - Minpuntos = 3
    - Maxpuntos = 25
    - Umbral = 0.05
"""

import parametros
import json
import os
from math import sqrt
from copy import copy



def main():

    #Leemos los parámetros que ha introducido el usuario    

    minimo_puntos = parametros.params.getMinPuntos()    
    maximo_puntos = parametros.params.getMaxPuntos()    
    umbral = parametros.params.getUmbral()    
    

    ###################
    # FICHERO PIERNAS #
    ###################
  
    numero_cluster = 0

    ficheroPiernas=open("clustersPiernas.json", "w")
    
    #Recorremos las carpetas con nombre positivo

    for filename in os.listdir('.'):
        if (os.path.isdir(filename) and "positivo" in filename):
            
            objetos=[]

            #Abrimos el archivo json de dentro de la carpeta

            for file in os.listdir(filename):
                if (file.endswith('json')):
                    a_abrir = file

            with open(filename+'/'+a_abrir, 'r') as f:
                for line in f:
                    objetos.append(json.loads(line))

            
            iterTotalesDict=objetos[len(objetos)-1]
            
            iterTotales=iterTotalesDict['Iteraciones totales']
            
            #Vamos leyendo los puntos del fichero y metiendolos en el cluster
            #dependiendo de los parametros maxPuntos, minPuntos y Umbral
            for i in range(iterTotales):
                x_elegidos = []
                y_elegidos = []
                
                puntosX=objetos[i+1]['PuntosX']
                puntosY=objetos[i+1]['PuntosY']
                
                #Recorremos los puntos de X e Y
                
                x_anterior = puntosX[0]
                y_anterior = puntosY[0]
                
                for px, py in zip(puntosX,puntosY):
                    
                    #Calculamos la distancia del punto 
                    distancia = sqrt( ((px-x_anterior)*(px-x_anterior)) + ((py-y_anterior)*(py-y_anterior)))  

                    #Si el punto leido pertenece a otro cluster
                    if (distancia > umbral or len(x_elegidos)+1 > maximo_puntos):
                        
                        #Miramos si el cluster actual tiene un minimo de puntos
                        #para poder guardarlo en el json
                        
                        if (len(x_elegidos) >= minimo_puntos):
                                        
                            cluster={"numero_cluster":numero_cluster,
                                      "numero_puntos":len(x_elegidos),
                                      "puntosX":copy(x_elegidos),
                                      "puntosY":copy(y_elegidos)}
                        
                            ficheroPiernas.write(json.dumps(cluster)+'\n')
                            numero_cluster += 1
                        
                        
                        x_elegidos.clear()
                        y_elegidos.clear()
                        

                    #Añadimos el nuevo punto al cluster
                    x_elegidos.append(px)
                    y_elegidos.append(py)
                        
                    x_anterior = px
                    y_anterior = py
                    
                #Si pasamos a la siguiente iteracion, miramos si podemos añadir
                #al json los puntos que tenemos hasta ese momento
                
                if (len(x_elegidos) >= minimo_puntos):
                                        
                    cluster={"numero_cluster":numero_cluster,
                             "numero_puntos":len(x_elegidos),
                             "puntosX":copy(x_elegidos),
                             "puntosY":copy(y_elegidos)}
                        
                    ficheroPiernas.write(json.dumps(cluster)+'\n')
                    numero_cluster += 1


    ficheroPiernas.close()    

    ######################
    # FICHERO NO PIERNAS #
    ######################
    
    numero_cluster = 0

    ficheroNoPiernas=open("clustersNoPiernas.json", "w")
    
    #Recorremos las carpetas con nombre negativo

    for filename in os.listdir('.'):
        if (os.path.isdir(filename) and "negativo" in filename):
            
            objetos=[]

            #Abrimos el archivo json de dentro de la carpeta

            for file in os.listdir(filename):
                if (file.endswith('json')):
                    a_abrir = file

            with open(filename+'/'+a_abrir, 'r') as f:
                for line in f:
                    objetos.append(json.loads(line))
            
            iterTotalesDict=objetos[len(objetos)-1]
            
            iterTotales=iterTotalesDict['Iteraciones totales']
            
            #Vamos leyendo los puntos del fichero y metiendolos en el cluster
            #dependiendo de los parametros maxPuntos, minPuntos y Umbral
            for i in range(iterTotales):
                x_elegidos = []
                y_elegidos = []
                
                puntosX=objetos[i+1]['PuntosX']
                puntosY=objetos[i+1]['PuntosY']
                
                #Recorremos los puntos de X e Y
                
                x_anterior = puntosX[0]
                y_anterior = puntosY[0]
                
                for px, py in zip(puntosX,puntosY):
                    
                    #Calculamos la distancia del punto 
                    distancia = sqrt( ((px-x_anterior)*(px-x_anterior)) + ((py-y_anterior)*(py-y_anterior)))  

                    #Si el punto leido pertenece a otro cluster
                    if (distancia > umbral or len(x_elegidos)+1 > maximo_puntos):
                        
                        #Miramos si el cluster actual tiene un minimo de puntos
                        #para poder guardarlo en el json
                        
                        if (len(x_elegidos) >= minimo_puntos):
                                        
                            cluster={"numero_cluster":numero_cluster,
                                      "numero_puntos":len(x_elegidos),
                                      "puntosX":copy(x_elegidos),
                                      "puntosY":copy(y_elegidos)}
                        
                            ficheroNoPiernas.write(json.dumps(cluster)+'\n')
                            numero_cluster += 1
                        
                        
                        x_elegidos.clear()
                        y_elegidos.clear()
                        

                    #Añadimos el nuevo punto al cluster
                    x_elegidos.append(px)
                    y_elegidos.append(py)
                        
                    x_anterior = px
                    y_anterior = py
                    
                #Si pasamos a la siguiente iteracion, miramos si podemos añadir
                #al json los puntos que tenemos hasta ese momento
                
                if (len(x_elegidos) >= minimo_puntos):
                                        
                    cluster={"numero_cluster":numero_cluster,
                             "numero_puntos":len(x_elegidos),
                             "puntosX":copy(x_elegidos),
                             "puntosY":copy(y_elegidos)}
                        
                    ficheroNoPiernas.write(json.dumps(cluster)+'\n')
                    numero_cluster += 1


    ficheroNoPiernas.close() 