#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Juan Emilio Martinez Manjon
Asignatura: Programacion Tecnica y Cientifica
Profesor: Eugenio Aguirre Molina
Curso: 2020/2021
"""

# mainInterfaz.py

"""
Este fichero genera la interfaz gráfica de la práctica usando tkinter y 
configura cada uno de los botones de la misma.
También creará las carpetas de positivos, negativos y predicciones al iniciarse.
Si no han sido creadas con antelación.
"""

from tkinter import *
from tkinter import messagebox
import vrep
import parametros 
import os
import capturar
import agrupar
import caracteristicas
import clasificarSVM
import predecir


#Tkinter
raiz = None

#Inicializacion global cajas
caja_iteraciones = None
caja_cerca = None
caja_media = None
caja_lejos = None
caja_maxpuntos = None
caja_minpuntos = None
caja_umbral = None

#Inicializacion global estado
etiqueta_estado = None

#Inicializacion global booleanos
conectado = False

#Inicializacion global listbox
listbox = None

#Inicializacion global botones
boton_desconectar = None
boton_capturar = None
boton_agrupar = None
boton_extraer = None
boton_entrenar = None
boton_predecir = None

#Variables vrep
clienteid = -1

#FUNCIONES DE CADA BOTON DE LA INTERFAZ

#Funcion que se activa cuando pulsamos el boton de conectar con VREP
def conectarPulsado():
    global conectado
    global etiqueta_estado
    global boton_capturar
    global boton_desconectar
    global clienteid
    
    
    if (conectado == True):
        messagebox.showwarning(message="La conexión con VREP ya ha sido establecida anteriormente")
    
    else:
        vrep.simxFinish(-1) 
        clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) 
 
        if clientID!=-1:
            messagebox.showinfo(message="Conexión con VREP establecida")
            conectado=True
            etiqueta_estado.config(text="Estado: Conectado a VREP")
            
            #Activamos los botones capturar y desconectar
            boton_capturar.config(state="normal")
            boton_desconectar.config(state="normal")
            clienteid = clientID
            parametros.params.setCliente(clienteid)
             
        else:
            messagebox.showerror(message="Debe iniciar el simulador")
            
            
            
#Funcion que se activa cuando pulsamos el boton de desconectar VREP
def desconectarPulsado():
    global clienteid
    global etiqueta_estado
    global boton_capturar
    global boton_desconectar
    global conectado
    
    #detenemos la simulacion
    vrep.simxStopSimulation(clienteid,vrep.simx_opmode_oneshot_wait)

    #cerramos la conexion
    vrep.simxFinish(clienteid) 
    
    #Cambiamos la etiqueta de estado
    etiqueta_estado.config(text="Estado: No conectado a VREP")
    
    #Deshabilitamos botones
    boton_capturar.config(state=DISABLED)
    boton_desconectar.config(state=DISABLED)
    
    #Informamos al usuario
    messagebox.showinfo(message="Se ha desconectado de VREP")
    
    conectado = False


    
    
#Funcion que se activa cuando pulsamos el boton de capturar
def capturarPulsado():
    global listbox
    global boton_agrupar
    
    #Comprobamos si hemos elegido algun item
    elegido = False
    
    for i in range(listbox.size()):
        if (listbox.selection_includes(i)):
            elegido = True
            
    if (elegido):
        
        #Si no existe el archivo, lo creamos
        if (not os.path.exists('./'+str(listbox.get(listbox.curselection()[0])))):
            
            if (messagebox.askyesno(message="Se va a crear el fichero: "+str(listbox.get(listbox.curselection()[0]))+" ¿Está seguro?")):
                with open(str(listbox.get(listbox.curselection()[0])), 'w') as json:
                    pass
        
        #Si existe, preguntamos si queremos sobreescribirlo
        else:
            if (messagebox.askyesno(message="El fichero: "+str(listbox.get(listbox.curselection()[0]))+" Ya existe. Se creará de nuevo. ¿Está seguro?")):
                os.remove(str(listbox.get(listbox.curselection()[0]))) 
                with open(str(listbox.get(listbox.curselection()[0])), 'w') as json:
                    pass

    
        #Llamamos al script Capturar.py con el nombre del fichero
        capturar.main(str(listbox.get(listbox.curselection()[0])))
        
        
        #Comprobamos si se han capturado todos los ficheros
        correcto = True
        
        for filename in os.listdir('.'):
            if (os.path.isdir(filename) and filename != 'prediccion' and filename != '__pycache__'):
                if (len(os.listdir(filename)) == 0):
                    correcto = False
                    
                elif(len(os.listdir(filename)) == 1): #Puede que sea la escena
                    for file in os.listdir(filename):
                        if (file.endswith('ttt')):
                            correcto = False


        #Habilitamos el boton de agrupar    
        if (correcto):
            boton_agrupar.config(state="normal")

        
    else:
        messagebox.showwarning(message="Debe elegir un fichero de la lista")
        
    
#Funcion que se activa cuando pulsamos el boton de capturar
def agruparPulsado():
    global boton_extraer
    
    agrupar.main()
    boton_extraer.config(state="normal")

    
    
#Funcion que se activa cuando pulsamos el boton de extraer
def extraerPulsado():
    global boton_entrenar

    caracteristicas.main()
    boton_entrenar.config(state="normal")
    
#Funcion que se activa cuando pulsamos el boton de entrenar
def entrenarPulsado():
    global boton_predecir
    
    clasificarSVM.main()
    boton_predecir.config(state="normal")
    
#Funcion que se activa cuando pulsamos el boton de predecir
def predecirPulsado():
    predecir.main()
    
#Funcion que se activa cuando pulsamos el boton de Salir
def salirPulsado():
    global conectado
    global raiz
    
    if (not conectado):
        
        if (messagebox.askyesno(message="¿Está seguro de que desea salir?")):
            raiz.destroy()
    
    else:
        messagebox.showwarning(message="Antes de salir debe desconectar")
    
#Funcion que se activa cuando pulsamos el boton de Cambiar
def cambiarPulsado():
    
    print("---- NUEVOS PARÁMETROS ----\n")
    
    #ITERACIONES
    global caja_iteraciones
    bien = True
    try:
        N = caja_iteraciones.get()
        N = int(N)
            
    except ValueError:
        messagebox.showerror(message="Las iteraciones deben ser números enteros")
        bien = False
    
    if (bien):
        parametros.params.setIteraciones(caja_iteraciones.get())
    
    print("Iteraciones:",parametros.params.getIteraciones())
    
    #CERCA
    global caja_cerca
    bien = True
    
    try:
        N = caja_cerca.get()
        N = float(N)
            
    except ValueError:
        messagebox.showerror(message="El parámetro cerca debe ser un número real")
        bien = False
    
    if (bien):
        parametros.params.setCerca(caja_cerca.get())
    
    print("Cerca:",parametros.params.getCerca())
    
    #MEDIA
    global caja_media
    bien = True
    
    try:
        N = caja_media.get()
        N = float(N)
            
    except ValueError:
        messagebox.showerror(message="El parámetro media debe ser un número real")
        bien = False
    
    if (bien):
        parametros.params.setMedia(caja_media.get())
    
    print("Media:",parametros.params.getMedia())
    
    #LEJOS
    global caja_lejos
    bien = True
    
    try:
        N = caja_lejos.get()
        N = float(N)
            
    except ValueError:
        messagebox.showerror(message="El parámetro lejos debe ser un número real")
        bien = False
    
    if (bien):
        parametros.params.setLejos(caja_lejos.get())
    
    print("Lejos:",parametros.params.getLejos())
    
    #MINPUNTOS
    global caja_minpuntos
    bien = True
    
    try:
        N = caja_minpuntos.get()
        N = int(N)
            
    except ValueError:
        messagebox.showerror(message="El parámetro minpuntos debe ser un número entero")
        bien = False
    
    if (bien):
        parametros.params.setMinPuntos(caja_minpuntos.get())
    
    print("Minpuntos:",parametros.params.getMinPuntos())
    
    
    #MAXPUNTOS
    global caja_maxpuntos
    bien = True
    
    try:
        N = caja_maxpuntos.get()
        N = int(N)
            
    except ValueError:
        messagebox.showerror(message="El parámetro maxpuntos debe ser un número entero")
        bien = False
    
    if (bien):
        parametros.params.setMaxPuntos(caja_maxpuntos.get())
    
    print("Maxpuntos:",parametros.params.getMaxPuntos())
    
    
    #UMBRAL
    global caja_umbral
    bien = True
    
    try:
        N = caja_umbral.get()
        N = float(N)
            
    except ValueError:
        messagebox.showerror(message="El parámetro umbral debe ser un número real")
        bien = False
    
    if (bien):
        parametros.params.setUmbral(caja_umbral.get())
    
    print("Umbral:",parametros.params.getUmbral(),"\n")
    

    


def crearcajaIteraciones(parent):
    global caja_iteraciones
    var = IntVar()
    var.set(50)
    caja_iteraciones = Entry(parent, textvariable=var, width=4)
    caja_iteraciones.grid(row=2,column=2)
    parametros.params.setIteraciones(caja_iteraciones.get())
    
def crearcajaCerca(parent):
    global caja_cerca
    var = DoubleVar()
    var.set(0.5)
    caja_cerca = Entry(parent, textvariable=var, width=4)
    caja_cerca.grid(row=3,column=2)
    parametros.params.setCerca(caja_cerca.get())
    
def crearcajaMedia(parent):
    global caja_media
    var = DoubleVar()
    var.set(1.5)
    caja_media = Entry(parent, textvariable=var, width=4)
    caja_media.grid(row=4,column=2)
    parametros.params.setMedia(caja_media.get())

def crearcajaLejos(parent):
    global caja_lejos
    var = DoubleVar()
    var.set(2.5)
    caja_lejos = Entry(parent, textvariable=var, width=4)
    caja_lejos.grid(row=5,column=2)
    parametros.params.setLejos(caja_lejos.get())

def crearcajaMinpuntos(parent):
    global caja_minpuntos
    var = IntVar()
    var.set(0)
    caja_minpuntos = Entry(parent, textvariable=var, width=4)
    caja_minpuntos.grid(row=6,column=2)
    parametros.params.setMinPuntos(caja_minpuntos.get())

def crearcajaMaxpuntos(parent):
    global caja_maxpuntos
    var = IntVar()
    var.set(0)
    caja_maxpuntos = Entry(parent, textvariable=var, width=4)
    caja_maxpuntos.grid(row=7,column=2)
    parametros.params.setMaxPuntos(caja_maxpuntos.get())

def crearcajaUmbral(parent):
    global caja_umbral
    var = IntVar()
    var.set(0)
    caja_umbral = Entry(parent, textvariable=var, width=4)
    caja_umbral.grid(row=8,column=2)
    parametros.params.setUmbral(caja_umbral.get())
    
    
def establecerEstado(parent):
    global etiqueta_estado
    etiqueta_estado = Label(parent, text="Estado: No conectado a VREP")
    etiqueta_estado.grid(row=3, column=0)
    
    
def crearBotonCapturar(parent):
    global boton_capturar
    boton_capturar = Button(parent, text="Capturar",state=DISABLED, command=capturarPulsado)
    boton_capturar.grid(row=4, column=0)  
    
def crearBotonAgrupar(parent):
    global boton_agrupar
    boton_agrupar = Button(parent, text="Agrupar",state=DISABLED, command=agruparPulsado)    
    boton_agrupar.grid(row=5, column=0)  
    
    
def crearBotonDesconectar(parent):
    global boton_desconectar
    boton_desconectar = Button(parent, text="Detener y desconectar VREP",state=DISABLED, command=desconectarPulsado)
    boton_desconectar.grid(row=2, column=0)  
    
    
def crearBotonExtraerCaracteristicas(parent):
    global boton_extraer
    boton_extraer = Button(parent, text="Extraer características",state=DISABLED, command=extraerPulsado)
    boton_extraer.grid(row=6, column=0) 
    
def crearBotonEntrenar(parent):
    global boton_entrenar
    #boton_entrenar = Button(parent, text="Entrenar clasificador",state=DISABLED, command=entrenarPulsado)
    boton_entrenar = Button(parent, text="Entrenar clasificador", command=entrenarPulsado)        
    boton_entrenar.grid(row=7, column=0) 
    
def crearBotonPredecir(parent):
    global boton_predecir
    #boton_predecir = Button(parent, text="Predecir",state=DISABLED, command=predecirPulsado)
    boton_predecir = Button(parent, text="Predecir",command=predecirPulsado)    
    boton_predecir.grid(row=8, column=0) 
    
    
def crearListBox(parent):
    global listbox
    listbox = Listbox(parent, width=35, height=13)
    listbox.insert(0,"positivo1/enPieCerca.json")    
    listbox.insert(1,"positivo2/enPieMedia.json")   
    listbox.insert(2,"positivo3/enPieLejos.json")   
    listbox.insert(3,"positivo4/sentadoCerca.json")   
    listbox.insert(4,"positivo5/sentadoMedia.json")   
    listbox.insert(5,"positivo6/sentadoLejos.json")   
    listbox.insert(6,"negativo1/cilindroMenorCerca.json")   
    listbox.insert(7,"negativo2/cilindroMenorMedia.json")   
    listbox.insert(8,"negativo3/cilindroMenorLejos.json")   
    listbox.insert(9,"negativo4/cilindroMayorCerca.json")   
    listbox.insert(10,"negativo5/cilindroMayorMedia.json")   
    listbox.insert(11,"negativo6/cilindroMayorLejos.json") 
    listbox.insert(12,"negativo7/cilindroMediaPared.json") 
    listbox.grid(row = 3, column=3,rowspan = 6)



def main():
    
    global raiz
    
    #Creamos las carpetas que se nos piden, si no existen ya
    
    for i in range(1,7):
        if (not os.path.exists('./positivo'+str(i))):
            os.mkdir('./positivo'+str(i))
            
    for i in range(1,8):
        if (not os.path.exists('./negativo'+str(i))):
            os.mkdir('./negativo'+str(i))
            
    if (not os.path.exists('./prediccion')):
        os.mkdir('./prediccion')
        
    
    #Creamos la interfaz grafica
    
    root = Tk()
    root.title("Práctica PTC Tkinter Robótica")
    root.geometry("700x300")
    
    #Ponemos la etiqueta de aviso
    etiqueta_aviso = Label(root, text="Es necesario ejecutar el simulador VREP")
    etiqueta_aviso.grid(row=0, column=0)
    
    #Boton de conectar con VREP
    boton_conectar = Button(root, text="Conectar con VREP", command=conectarPulsado)
    boton_conectar.grid(row=1, column=0)    
    
    #Boton detener y desconectar VREP
    crearBotonDesconectar(root)
    
    #Etiqueta de estado de la conexion
    establecerEstado(root)
    
    #Boton capturar
    crearBotonCapturar(root)
    
    #Boton agrupar
    crearBotonAgrupar(root)
    
    #Boton extraer caracteristicas
    crearBotonExtraerCaracteristicas(root)
    
    #Boton entrenar clasificador
    crearBotonEntrenar(root)
    
    #Boton predecir
    crearBotonPredecir(root)
    
    #Boton Salir
    boton_salir = Button(root, text="Salir", command=salirPulsado)
    boton_salir.grid(row=9, column=0)  
    
    #Ponemos la etiqueta de Parámetros
    etiqueta_parametros = Label(root, text="Parámetros")
    etiqueta_parametros.grid(sticky="E",row=1, column=1)
    
    #Ponemos la etiqueta de iteraciones
    etiqueta_iteraciones = Label(root, text="Iteraciones:")
    etiqueta_iteraciones.grid(sticky="E",row=2, column=1)
    
    #Ponemos la etiqueta de cerca
    etiqueta_cerca = Label(root, text="Cerca:")
    etiqueta_cerca.grid(sticky="E",row=3, column=1)
    
    #Ponemos la etiqueta de media
    etiqueta_media = Label(root, text="Media:")
    etiqueta_media.grid(sticky="E",row=4, column=1)
    
    #Ponemos la etiqueta de lejos
    etiqueta_lejos = Label(root, text="Lejos:")
    etiqueta_lejos.grid(sticky="E",row=5, column=1)
    
    #Ponemos la etiqueta de minpuntos
    etiqueta_minpuntos = Label(root, text="MinPuntos:")
    etiqueta_minpuntos.grid(sticky="E",row=6, column=1)
    
    #Ponemos la etiqueta de maxpuntos
    etiqueta_maxpuntos = Label(root, text="MaxPuntos:")
    etiqueta_maxpuntos.grid(sticky="E",row=7, column=1)
    
    #Ponemos la etiqueta de umbral
    etiqueta_umbral = Label(root, text="UmbralDistancia:")
    etiqueta_umbral.grid(sticky="E",row=8, column=1)
    
    #Boton Cambiar
    boton_cambiar = Button(root, text="Cambiar", command=cambiarPulsado)
    boton_cambiar.grid(row=9, column=1)  
    
    #Caja de texto iteraciones
    crearcajaIteraciones(root)
    
    #Caja de texto cerca
    crearcajaCerca(root)
    
    #Caja de texto media
    crearcajaMedia(root)
    
    #Caja de texto lejos
    crearcajaLejos(root)
    
    #Caja de texto minpuntos
    crearcajaMinpuntos(root)
    
    #Caja de texto maxpuntos
    crearcajaMaxpuntos(root)
    
    #Caja de texto umbral
    crearcajaUmbral(root)
    
    #Ponemos la etiqueta de fichero para la captura
    etiqueta_fichero = Label(root, text="Fichero para la captura")
    etiqueta_fichero.grid(row=1, column=3)
    
    #Creamos la listbox con los ficheros positivos y negativos
    crearListBox(root)
    
    raiz = root
    root.mainloop()
    
main()