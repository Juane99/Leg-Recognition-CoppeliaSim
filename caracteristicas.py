#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Juan Emilio Martinez Manjon
Asignatura: Programacion Tecnica y Cientifica
Profesor: Eugenio Aguirre Molina
Curso: 2020/2021
"""

# caracteristicas.py

"""
Este fichero usa los clusters creados en el fichero agrupar.py para extraer
3 características de cada uno. En concreto calculará la anchura, la profundidad
y el perímetro. Después creará dos archivos .dat con dichas características,
uno para los ejemplos positivos y otro para los negativos.
"""

import json
import csv
from math import sqrt

def main():
    
    ###################
    # FICHERO PIERNAS #
    ###################
    
    ficheroPiernas=open("caracteristicasPiernas.dat", "w")
    
    #Leemos todos los diccionarios del fichero clustersPiernas.json
    
    objetos = []
    
    with open("clustersPiernas.json", 'r') as f:
        for line in f:
            objetos.append(json.loads(line))
    
    for diccionario in objetos:
        
        numero_cluster = diccionario["numero_cluster"]
        
        #Calculamos su perimetro sumando las distancias entre todos los puntos        
        perimetro = 0
        
        x_anterior = (diccionario["puntosX"])[0]
        y_anterior = (diccionario["puntosY"])[0]

        for x,y in zip(diccionario["puntosX"],diccionario["puntosY"]):
            distancia = sqrt( ((x-x_anterior)*(x-x_anterior)) + ((y-y_anterior)*(y-y_anterior)))             
            perimetro += distancia
            x_anterior = x
            y_anterior = y
            
        
        #Calculamos la anchura mediante la distancia del primer punto
        #del cluster al último
        
        ultima_x = (diccionario["puntosX"])[len(diccionario["puntosX"])-1]
        ultima_y = (diccionario["puntosY"])[len(diccionario["puntosY"])-1]

        primera_x = (diccionario["puntosX"])[0]
        primera_y = (diccionario["puntosY"])[0]


        anchura = sqrt((ultima_x-primera_x)*(ultima_x-primera_x) + (ultima_y-primera_y)*(ultima_y-primera_y))    
        
        #Calculamos la profundidad calculando la recta que va del primer
        #punto del cluster al último. Luego calcularemos la distancia de todos
        #los puntos a esa recta y nos quedaremos con la mayor de todas.
    
        
        p_maxima = 0
        
        #Recta entre el primero y el ultimo
        A = ultima_y-primera_y
        B = -1*(ultima_x - primera_x)
        C = -1 * primera_x * (ultima_y-primera_y) + primera_y * (ultima_x-primera_x)
        
        for x,y in zip(diccionario["puntosX"],diccionario["puntosY"]):

            p = abs((A * x + B * y + C)) / (sqrt(A * A + B * B))
    
            if (p > p_maxima):
                p_maxima = p
                
                
        #Escribimos la caracteristicas en el .dat
        caracteristicas={"numero_cluster":numero_cluster,
                        "perimetro":perimetro,
                        "profundidad":p_maxima,
                        "anchura":anchura,
                        "esPierna":1}
        
        ficheroPiernas.write(str(caracteristicas))
        ficheroPiernas.write('\n')
    
    ficheroPiernas.close()
    
    
    ######################
    # FICHERO NO PIERNAS #
    ######################
    
    ficheroNoPiernas=open("caracteristicasNoPiernas.dat", "w")
    
    #Leemos todos los diccionarios del fichero clustersPiernas.json
    
    objetos = []
    
    with open("clustersNoPiernas.json", 'r') as f:
        for line in f:
            objetos.append(json.loads(line))
    
    for diccionario in objetos:
        
        numero_cluster = diccionario["numero_cluster"]
        
        #Calculamos su perimetro sumando las distancias entre todos los puntos        
        perimetro = 0
        
        x_anterior = (diccionario["puntosX"])[0]
        y_anterior = (diccionario["puntosY"])[0]

        for x,y in zip(diccionario["puntosX"],diccionario["puntosY"]):
            distancia = sqrt( ((x-x_anterior)*(x-x_anterior)) + ((y-y_anterior)*(y-y_anterior)))             
            perimetro += distancia
            x_anterior = x
            y_anterior = y
            
        
        #Calculamos la anchura mediante la distancia del primer punto del cluster
        #al último
        
        ultima_x = (diccionario["puntosX"])[len(diccionario["puntosX"])-1]
        ultima_y = (diccionario["puntosY"])[len(diccionario["puntosY"])-1]

        primera_x = (diccionario["puntosX"])[0]
        primera_y = (diccionario["puntosY"])[0]


        anchura = sqrt((ultima_x-primera_x)*(ultima_x-primera_x) + (ultima_y-primera_y)*(ultima_y-primera_y))    
        
        #Calculamos la profundidad calculando la recta que va del primer
        #punto del cluster al último. Luego calcularemos la distancia de todos
        #los puntos a esa recta y nos quedaremos con la mayor de todas.        
        
        p_maxima = 0
        
        #Recta entre el primero y el ultimo
        A = ultima_y-primera_y
        B = -1*(ultima_x - primera_x)
        C = -1 * primera_x * (ultima_y-primera_y) + primera_y * (ultima_x-primera_x)
        
        for x,y in zip(diccionario["puntosX"],diccionario["puntosY"]):

            p = abs((A * x + B * y + C)) / (sqrt(A * A + B * B))
    
            if (p > p_maxima):
                p_maxima = p
                
                
        #Escribimos la caracteristicas en el .dat
        caracteristicas={"numero_cluster":numero_cluster,
                        "perimetro":perimetro,
                        "profundidad":p_maxima,
                        "anchura":anchura,
                        "esPierna":0}
        
        ficheroNoPiernas.write(str(caracteristicas))
        ficheroNoPiernas.write('\n')
    
    ficheroNoPiernas.close()
    
    
    #Creamos el fichero CSV final
    
    with open('piernasDataset.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        
        #Primero escribimos todos los ejemplos negativos
            
        with open("caracteristicasNoPiernas.dat", 'r') as f:
            for line in f:                
                line = line.replace("'", '"') 
                line = json.loads(line) 
                caracteristica = [line["perimetro"],line["profundidad"],line["anchura"],line["esPierna"]]
                writer.writerow(caracteristica)
                
                
        #Ahora los ejemplos positivos
        
        with open("caracteristicasPiernas.dat", 'r') as f:
            for line in f:
                line = line.replace("'", '"') 
                line = json.loads(line) 
                caracteristica = [line["perimetro"],line["profundidad"],line["anchura"],line["esPierna"]]
                writer.writerow(caracteristica)