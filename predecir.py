#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Juan Emilio Martinez Manjon
Asignatura: Programacion Tecnica y Cientifica
Profesor: Eugenio Aguirre Molina
Curso: 2020/2021
"""

# predecir.py

"""
Este fichero usa la escena de test y replica todo lo visto en los ficheros
de agrupar y extraer caracteristicas para obtener datos que pueda usar
nuestro clasificador.

Una vez obtenidas las etiquetas por parte del clasificador pintaremos
en un gráfico las piernas de color rojo y los cilindros/paredes de color azul.
"""

import vrep
import time
import parametros 
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
from copy import copy
from sklearn.metrics import accuracy_score


def main():
    
    #Primero vamos a recibir los puntos que capture el robot de la escena
    #de test
    
    
    #Guardar la referencia al robot
    _, robothandle = vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
            
    #Guardar la referencia de los motores
    _, left_motor_handle=vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    _, right_motor_handle=vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
     
    #Guardar la referencia de la camara
    _, camhandle = vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
     
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(parametros.params.getCliente(),'LaserData',vrep.simx_opmode_streaming)    
    
    #Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(parametros.params.getCliente(), camhandle, 0, vrep.simx_opmode_streaming)
            
    time.sleep(5) 
    
    puntosx=[] 
    puntosy=[]
    puntosz=[]

    returnCode, signalValue = vrep.simxGetStringSignal(parametros.params.getCliente(),'LaserData',vrep.simx_opmode_buffer) 
       
    datosLaser=vrep.simxUnpackFloats(signalValue)
    for indice in range(0,len(datosLaser),3):
        puntosx.append(datosLaser[indice+1])
        puntosy.append(datosLaser[indice+2])
        puntosz.append(datosLaser[indice])

      
    
    #Una vez tenemos los puntos, los convertimos en clusters usando el mismo
    #proceso que en el fichero agrupar.py
    
    clusters = []
    
    umbral = parametros.params.getUmbral()
    maximo_puntos = parametros.params.getMaxPuntos()
    minimo_puntos = parametros.params.getMinPuntos()
    numero_cluster = 0
    
    x_elegidos = []
    y_elegidos = []
                
                
    #Recorremos los puntos de X e Y
                
    x_anterior = puntosx[0]
    y_anterior = puntosy[0]
                
    
    
    for px, py in zip(puntosx,puntosy):
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
                
                        
                clusters.append(cluster)
                numero_cluster += 1
                        
                        
            x_elegidos.clear()
            y_elegidos.clear()
                        

        #Añadimos el nuevo punto al cluster
        x_elegidos.append(px)
        y_elegidos.append(py)
                                
        x_anterior = px
        y_anterior = py

                    
    #Miramos si podemos añadir los puntos que tenemos hasta ese momento
    #antes de terminar.
          
    if (len(x_elegidos) >= minimo_puntos):
                                        
        cluster={"numero_cluster":numero_cluster,
                 "numero_puntos":len(x_elegidos),
                 "puntosX":copy(x_elegidos),
                 "puntosY":copy(y_elegidos)}
                        
        clusters.append(cluster)
        numero_cluster += 1
      
        
    #Generamos las 3 características de cada cluster usando el mismo
    #procedimiento que en el fichero caracteristicas.py
    
    lista_caracteristicas = []
            
    for diccionario in clusters:
        
        
        numero_cluster = diccionario["numero_cluster"]
        
        #Calculamos su perimetro sumando las distancias entre todos los puntos        
        perimetro = 0.0
        
        x_anterior = (diccionario["puntosX"])[0]
        y_anterior = (diccionario["puntosY"])[0]

        for x,y in zip(diccionario["puntosX"],diccionario["puntosY"]):
            distancia = sqrt( ((x-x_anterior)*(x-x_anterior)) + ((y-y_anterior)*(y-y_anterior)))             
            perimetro += distancia
            x_anterior = x
            y_anterior = y
            
        
        #Calculamos la anchura mediante la distancia del primer punto del
        #cluster al último.
        
        ultima_x = (diccionario["puntosX"])[len(diccionario["puntosX"])-1]
        ultima_y = (diccionario["puntosY"])[len(diccionario["puntosY"])-1]

        primera_x = (diccionario["puntosX"])[0]
        primera_y = (diccionario["puntosY"])[0]


        anchura = sqrt( ((ultima_x-primera_x)*(ultima_x-primera_x)) + ((ultima_y-primera_y)*(ultima_y-primera_y)))    
        
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
                
                
        #Guardamos las caracteristicas en una lista
        caracteristicas={"numero_cluster":numero_cluster,
                        "perimetro":perimetro,
                        "profundidad":p_maxima,
                        "anchura":anchura}
        
        lista_caracteristicas.append(caracteristicas)


    #Convertimos las caracteristicas a un formato legible por el clasificador
    
    caracteristicas_finales = []
    
    for caracteristica in lista_caracteristicas:
        carac = [caracteristica["perimetro"],caracteristica["profundidad"],caracteristica["anchura"]]
        caracteristicas_finales.append(carac)

        
    #Pasamos a clasificar los clusters según sus características
    
    # Leemos el clasificador
    with open("clasificador.pkl", "rb") as archivo:
        clasificador=pickle.load(archivo)
        

    #Usamos un DataFrame de Pandas para pasar nuestra lista de caracteristicas
    #a un formato legible y poder predecir sobre ellas.
    
    y_test = [1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0]    
    
    caracteristicas_finales = np.array(caracteristicas_finales)
    carDataF = pd.DataFrame(caracteristicas_finales)
    
    prediccion = clasificador.predict(carDataF)
    acc_test=accuracy_score(y_test, prediccion)
    prediccion = list(prediccion)
    
    print(prediccion)
    print("Accuracy: ", acc_test)
    
    
    #Representamos graficamente las predicciones
    
    #Primero guardamos en listas los puntos que van a ir en rojo, y los
    #que van a ir en azul
    
    puntos_rojosx = []
    puntos_rojosy = []
    puntos_azulx = []
    puntos_azuly = []
    
    contador = 0
    for diccionario in clusters:
        
        if (prediccion[contador] == 0): #No es pierna
        
            for px in diccionario["puntosX"]:
                puntos_azulx.append(px)

            for py in diccionario["puntosY"]:
                puntos_azuly.append(py)
        else: #Si es pierna
            for px in diccionario["puntosX"]:
                puntos_rojosx.append(px)

            for py in diccionario["puntosY"]:
                puntos_rojosy.append(py) 
            
        contador += 1
    
    
    #Calculamos los puntos del centro de los objetos según las predicciones
    #Primero sacamos los centroides de todos los clusters
    
    centroides = []
    
    for clu in clusters:
        centroide_x = sum(clu["puntosX"])/len(clu["puntosX"])
        centroide_y = sum(clu["puntosY"])/len(clu["puntosY"])
        centroides.append((centroide_x,centroide_y))
    
    
    #Ahora obtenemos el punto del centro de los objetos en función de los
    #centroides
    
    puntos_medios_x_azul = []
    puntos_medios_y_azul = []
    puntos_medios_x_rojo = []
    puntos_medios_y_rojo = []
    

    #Vamos obteniendo la distancia de cada centroide a los demas y pintaremos
    #un punto en el centro del segmento que unen dichos centroides si su 
    #distancia es menor a 0.5 metros. Este dato lo he obtenido empíricamente
    #viendo la distancia entre dos piernas de una misma persona.
    
    for i in range(0, len(centroides)-1):
        
        
        distancia_minima = sqrt( (((centroides[i+1])[0]-(centroides[i])[0])*((centroides[i+1])[0]-(centroides[i])[0])) + (((centroides[i+1])[1]-(centroides[i])[1])*((centroides[i+1])[1]-(centroides[i])[1])))             
        mejor_pareja = centroides[i+1]
        pos_mejor_pareja = i+1
        
        
        for j in range(i+1, len(centroides)):
            distancia = sqrt( (((centroides[j])[0]-(centroides[i])[0])*((centroides[j])[0]-(centroides[i])[0])) + (((centroides[j])[1]-(centroides[i])[1])*((centroides[j])[1]-(centroides[i])[1])))             
    
            if (distancia < distancia_minima and prediccion[j] == prediccion[i]):
                distancia_minima = distancia
                mejor_pareja = centroides[j]
                pos_mejor_pareja = j

            
        
        if (distancia_minima < 0.5):
            media_x = ((mejor_pareja)[0] + (centroides[i])[0])/2
            media_y = ((mejor_pareja)[1] + (centroides[i])[1])/2
            
            if (prediccion[i] == 0): #Si es un cilindro
                puntos_medios_x_azul.append(media_x)
                puntos_medios_y_azul.append(media_y)
                
            else:
                puntos_medios_x_rojo.append(media_x)
                puntos_medios_y_rojo.append(media_y)


    
    plt.axis('equal')
    plt.axis([0, 4, -2, 2])  
    
    plt.clf()    
    plt.plot(puntos_rojosx, puntos_rojosy, 'r.')
    plt.plot(puntos_azulx, puntos_azuly, 'b.')
    plt.plot(puntos_medios_x_azul, puntos_medios_y_azul, 'b.', markersize=8)
    plt.plot(puntos_medios_x_rojo, puntos_medios_y_rojo, 'r.', markersize=8)
    plt.savefig('prediccion/fichero.jpg')
    plt.show()
    