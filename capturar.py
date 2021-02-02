#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Juan Emilio Martinez Manjon
Asignatura: Programacion Tecnica y Cientifica
Profesor: Eugenio Aguirre Molina
Curso: 2020/2021
"""

# capturar.py

"""
Este fichero captura varios puntos usando la escena cargada en el simulador
y guarda los resultados en el fichero que se le pasa como parámetro al
script
"""

from math import cos,sin,pi
import parametros 
import vrep
import time
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os


def main(fichero_entrada):

    
    directorio = (fichero_entrada).split('/')
    
    #Cambiamos al directorio que se le pasa como parámetro
    os.chdir(directorio[0])
    
    #Guardar la referencia al robot
    
    _, robothandle = vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
            
    #Guardar la referencia de los motores
    _, left_motor_handle=vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
    _, right_motor_handle=vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
     
    #Guardar la referencia de la camara
    _, camhandle = vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
     
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(parametros.params.getCliente(),'LaserData',vrep.simx_opmode_streaming)
    
    velocidad = 0 #Variable para la velocidad de los motores, dejamos fijo el robot
    
    #Dependiendo del fichero que le metamos como parametro, vamos a tomar la referencia
    #de Bill o de los cilindros (Cylinder y Cylinder0)
    
    if ((fichero_entrada).startswith("positivo")):
        _, personhandle = vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Bill', vrep.simx_opmode_oneshot_wait)
    
    else:
        _, cilindro1 = vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Cylinder', vrep.simx_opmode_oneshot_wait)
        _, cilindro2 = vrep.simxGetObjectHandle(parametros.params.getCliente(), 'Cylinder0', vrep.simx_opmode_oneshot_wait)
    
    
    #Iniciar la camara y esperar un segundo para llenar el buffer
    _, resolution, image = vrep.simxGetVisionSensorImage(parametros.params.getCliente(), camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
     
    plt.axis('equal')
    plt.axis([0, 4, -2, 2])  
    
    
    #Creamos el fichero JSON para guardar los datos del laser
    #usamos diccionarios
    segundos=5
    maxIter= parametros.params.getIteraciones()
    iteracion=0
    
    cabecera={"TiempoSleep":segundos,
              "MaxIteraciones":maxIter}
    
    nombre_fichero = (fichero_entrada).split('/')
    ficheroLaser=open(nombre_fichero[1], "w")
    
    ficheroLaser.write(json.dumps(cabecera)+'\n')
    
    seguir=True
    
    t = 0.5*pi
    
    while(iteracion <= maxIter and seguir):
        
        #Miramos si estamos en el caso de cerca, media o lejos
        
        if ("Cerca" in nombre_fichero[1]):
            
            #Comprobamos si estamos en el caso de positivos o negativos
            
            if ((fichero_entrada).startswith("positivo")):
                returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),personhandle,-1,[parametros.params.getCerca()+iteracion*((parametros.params.getMedia()-parametros.params.getCerca())/parametros.params.getIteraciones()),0.0,0.0],vrep.simx_opmode_oneshot)
                returnCode = vrep.simxSetObjectOrientation(parametros.params.getCliente(), personhandle, -1, [0.0,0.0,3.05-(0.20)*iteracion], vrep.simx_opmode_oneshot)
            else:
                
                if ("1" in nombre_fichero[0] or "2" in nombre_fichero[0] or "3" in nombre_fichero[0]):
                    centro = parametros.params.getCerca()+iteracion*((parametros.params.getMedia()-parametros.params.getCerca())/parametros.params.getIteraciones())
                    
                    #Vamos moviendo los cilindros en el eje x al mismo tiempo
                    #que los vamos rotando usando las ecuaciones de la 
                    #circunferencia
                    
                    
                    x1 = -0.075*cos(t%(2*pi))+centro
                    y1 = -0.075*sin(t%(2*pi))
                    
                    x2 = 0.075*cos(t%(2*pi))+centro
                    y2 = 0.075*sin(t%(2*pi))
                    
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro1,-1,[x1,y1,0.5],vrep.simx_opmode_oneshot)
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro2,-1,[x2,y2,0.5],vrep.simx_opmode_oneshot)
                    
                    t = t + 0.2
                    
                else:
                    
                    centro = parametros.params.getCerca()+iteracion*((parametros.params.getMedia()-parametros.params.getCerca())/parametros.params.getIteraciones())
                
                    #Vamos moviendo los cilindros en el eje x al mismo tiempo
                    #que los vamos rotando usando las ecuaciones de la 
                    #circunferencia     
                    
                    x1 = -0.125*cos(t%(2*pi))+centro
                    y1 = -0.125*sin(t%(2*pi))
                    
                    x2 = 0.125*cos(t%(2*pi))+centro
                    y2 = 0.125*sin(t%(2*pi))
                    
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro1,-1,[x1,y1,0.5],vrep.simx_opmode_oneshot)
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro2,-1,[x2,y2,0.5],vrep.simx_opmode_oneshot)
                    
                    t = t + 0.2
                
               
        elif ("Media" in nombre_fichero[1]):
           
            #Comprobamos si estamos en el caso de positivos o negativos
            if ((fichero_entrada).startswith("positivo")):
                returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),personhandle,-1,[parametros.params.getMedia()+iteracion*((parametros.params.getLejos()-parametros.params.getMedia())/parametros.params.getIteraciones()),0.0,0.0],vrep.simx_opmode_oneshot)
                returnCode = vrep.simxSetObjectOrientation(parametros.params.getCliente(), personhandle, -1, [0.0,0.0,3.05-(0.20)*iteracion], vrep.simx_opmode_oneshot)
    
            else:
            
                    
                if ("1" in nombre_fichero[0] or "2" in nombre_fichero[0] or "3" in nombre_fichero[0]):
                    centro = parametros.params.getMedia()+iteracion*((parametros.params.getLejos()-parametros.params.getMedia())/parametros.params.getIteraciones())
                    
                    #Vamos moviendo los cilindros en el eje x al mismo tiempo
                    #que los vamos rotando usando las ecuaciones de la 
                    #circunferencia
                    
                    x1 = -0.075*cos(t%(2*pi))+centro
                    y1 = -0.075*sin(t%(2*pi))
                    
                    x2 = 0.075*cos(t%(2*pi))+centro
                    y2 = 0.075*sin(t%(2*pi))
                    
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro1,-1,[x1,y1,0.5],vrep.simx_opmode_oneshot)
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro2,-1,[x2,y2,0.5],vrep.simx_opmode_oneshot)
                    
                    t = t + 0.2
                    
                else:
                    
                    centro = parametros.params.getMedia()+iteracion*((parametros.params.getLejos()-parametros.params.getMedia())/parametros.params.getIteraciones())
                    
                    #Vamos moviendo los cilindros en el eje x al mismo tiempo
                    #que los vamos rotando usando las ecuaciones de la 
                    #circunferencia
                    
                    x1 = -0.125*cos(t%(2*pi))+centro
                    y1 = -0.125*sin(t%(2*pi))
                    
                    x2 = 0.125*cos(t%(2*pi))+centro
                    y2 = 0.125*sin(t%(2*pi))
                    
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro1,-1,[x1,y1,0.5],vrep.simx_opmode_oneshot)
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro2,-1,[x2,y2,0.5],vrep.simx_opmode_oneshot)
                    
                    t = t + 0.2                 
                
        elif ("Lejos" in nombre_fichero[1]):
           
            #Comprobamos si estamos en el caso de positivos o negativos
            
            if ((fichero_entrada).startswith("positivo")):
                returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),personhandle,-1,[parametros.params.getLejos()+iteracion*((parametros.params.getLejos()+1-parametros.params.getLejos())/parametros.params.getIteraciones()),0.0,0.0],vrep.simx_opmode_oneshot)
                returnCode = vrep.simxSetObjectOrientation(parametros.params.getCliente(), personhandle, -1, [0.0,0.0,3.05-(0.20)*iteracion], vrep.simx_opmode_oneshot)
    
            else:
    
                if ("1" in nombre_fichero[0] or "2" in nombre_fichero[0] or "3" in nombre_fichero[0]):
                    centro = parametros.params.getLejos()+iteracion*((parametros.params.getLejos()+1-parametros.params.getLejos())/parametros.params.getIteraciones())
                    
                    #Vamos moviendo los cilindros en el eje x al mismo tiempo
                    #que los vamos rotando usando las ecuaciones de la 
                    #circunferencia
                    
                    x1 = -0.075*cos(t%(2*pi))+centro
                    y1 = -0.075*sin(t%(2*pi))
                    
                    x2 = 0.075*cos(t%(2*pi))+centro
                    y2 = 0.075*sin(t%(2*pi))
                    
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro1,-1,[x1,y1,0.5],vrep.simx_opmode_oneshot)
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro2,-1,[x2,y2,0.5],vrep.simx_opmode_oneshot)
                    
                    t = t + 0.2
                    
                else:
                    
                    centro = parametros.params.getLejos()+iteracion*((parametros.params.getLejos()+1-parametros.params.getLejos())/parametros.params.getIteraciones())
                    
                    #Vamos moviendo los cilindros en el eje x al mismo tiempo
                    #que los vamos rotando usando las ecuaciones de la 
                    #circunferencia                    
                    
                    x1 = -0.125*cos(t%(2*pi))+centro
                    y1 = -0.125*sin(t%(2*pi))
                    
                    x2 = 0.125*cos(t%(2*pi))+centro
                    y2 = 0.125*sin(t%(2*pi))
                    
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro1,-1,[x1,y1,0.5],vrep.simx_opmode_oneshot)
                    returnCode = vrep.simxSetObjectPosition(parametros.params.getCliente(),cilindro2,-1,[x2,y2,0.5],vrep.simx_opmode_oneshot)
                    
                    t = t + 0.2                      
    
    
    
        time.sleep(segundos) #esperamos un tiempo para que el ciclo de lectura de datos no sea muy rápido
        
        puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
        puntosy=[]
        puntosz=[]
        returnCode, signalValue = vrep.simxGetStringSignal(parametros.params.getCliente(),'LaserData',vrep.simx_opmode_buffer) 
       
        datosLaser=vrep.simxUnpackFloats(signalValue)
        for indice in range(0,len(datosLaser),3):
            puntosx.append(datosLaser[indice+1])
            puntosy.append(datosLaser[indice+2])
            puntosz.append(datosLaser[indice])
        
        print("Iteración: ", iteracion)        
        plt.clf()    
        plt.plot(puntosx, puntosy, 'r.')
        plt.show()
        
        #Guardamos los puntosx, puntosy en el fichero JSON
        lectura={"Iteracion":iteracion, "PuntosX":puntosx, "PuntosY":puntosy}
        ficheroLaser.write(json.dumps(lectura)+'\n')
        
        #Guardar frame de la camara, rotarlo y convertirlo a BGR
        _, resolution, image=vrep.simxGetVisionSensorImage(parametros.params.getCliente(), camhandle, 0, vrep.simx_opmode_buffer)
        img = np.array(image, dtype = np.uint8)
        img.resize([resolution[0], resolution[1], 3])
        img = np.rot90(img,2)
        img = np.fliplr(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
     
         
        #Convertir img a hsv y detectar colores
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        verde_bajos = np.array([49,50,50], dtype=np.uint8)
        verde_altos = np.array([80, 255, 255], dtype=np.uint8)
        mask = cv2.inRange(hsv, verde_bajos, verde_altos) #Crear mascara
     
        #Limpiar mascara y buscar centro del objeto verde
        moments = cv2.moments(mask)
        area = moments['m00']
        if(area > 200):
            x = int(moments['m10']/moments['m00'])
            y = int(moments['m01']/moments['m00'])
            cv2.rectangle(img, (x, y), (x+2, y+2),(0,0,255), 2)
            #Descomentar para printear la posicion del centro
            #print(x,y)
     
            #Si el centro del objeto esta en la parte central de la pantalla (aprox.), detener motores
            if abs(x-256/2) < 15:
                vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), left_motor_handle,0,vrep.simx_opmode_streaming)
                vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), right_motor_handle,0,vrep.simx_opmode_streaming)
     
            #Si no, girar los motores hacia la derecha o la izquierda
            elif x > 256/2:
                vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), left_motor_handle,velocidad,vrep.simx_opmode_streaming)
                vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), right_motor_handle,-velocidad,vrep.simx_opmode_streaming)
            elif x < 256/2:
                vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), left_motor_handle,-velocidad,vrep.simx_opmode_streaming)
                vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), right_motor_handle,velocidad,vrep.simx_opmode_streaming)
           
        
        #Si estamos en la primera iteracion, guardamos la imagen
        if (iteracion == 1):
            cv2.imwrite(((nombre_fichero[1]).split('.'))[0]+str(iteracion-1)+'.jpg', img)
         
        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            seguir=False
        
        #Dejamos 0.5 segundos de tiempo de espera
        time.sleep(0.5)
        iteracion=iteracion+1
        
    vr=1 #en rad/seg son unos 57 g/s
    
    
    #movemos el robot
    vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), left_motor_handle,vr,vrep.simx_opmode_oneshot )
    vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), right_motor_handle,vr,vrep.simx_opmode_oneshot )
    
    
    time.sleep(4)
    
    # lo paramos
    
    vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), left_motor_handle,0,vrep.simx_opmode_oneshot)
    vrep.simxSetJointTargetVelocity(parametros.params.getCliente(), right_motor_handle,0,vrep.simx_opmode_oneshot)
    
    time.sleep(1)
    
    #vemos la velocidad actual
    
    velocidadIz=vrep.simxGetObjectVelocity(parametros.params.getCliente(), left_motor_handle,vrep.simx_opmode_oneshot_wait)
    velocidadDe=vrep.simxGetObjectVelocity(parametros.params.getCliente(), right_motor_handle,vrep.simx_opmode_oneshot_wait)
    
    print("\nVelocidad iz: ", velocidadIz, "\nVelocidad de:", velocidadDe)
    
    posicionRobot=vrep.simxGetObjectPosition(parametros.params.getCliente(), robothandle, -1, vrep.simx_opmode_oneshot_wait)
    
    print("\n La posicion es: ", posicionRobot)
    
    orientacionRobot=vrep.simxGetObjectOrientation(parametros.params.getCliente(), robothandle, -1, vrep.simx_opmode_oneshot_wait)
    
    print("\n La orientacion es: ", orientacionRobot)
    
    
    #cerramos las ventanas
    cv2.destroyAllWindows()
    
    
    finFichero={"Iteraciones totales":iteracion-1}
    ficheroLaser.write(json.dumps(finFichero)+'\n')
    ficheroLaser.close()
    
    #salvo a disco la ultima imagen
    cv2.imwrite(((nombre_fichero[1]).split('.'))[0]+str(iteracion-1)+'.jpg', img)

    #Cambiamos al directorio anterior de nuevo
    os.chdir('..')
