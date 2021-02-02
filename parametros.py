#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Juan Emilio Martinez Manjon
Asignatura: Programacion Tecnica y Cientifica
Profesor: Eugenio Aguirre Molina
Curso: 2020/2021
"""

# parametros.py

"""
Este fichero crea la clase parametros y los va guardando. Podremos acceder
a ellos desde los diferentes ficheros .py de la práctica.
"""

class Parametros:
    def __init__(self):
        self.iteraciones = int(50)
        self.cerca = float(0.5)
        self.media = float(1.5)
        self.lejos = float(2.5)
        self.minpuntos = int(0)
        self.maxpuntos = int(0)
        self.umbraldistancia = float(0.0)
        self.cliente = int(-1)

    
    def getIteraciones(self):
        return self.iteraciones
    
    def getCerca(self):
        return self.cerca

    def getMedia(self):
        return self.media
    
    def getLejos(self):
        return self.lejos
    
    def getMinPuntos(self):
        return self.minpuntos
    
    def getMaxPuntos(self):
        return self.maxpuntos
    
    def getUmbral(self):
        return self.umbraldistancia
    
    def getCliente(self):
        return self.cliente

    def setIteraciones(self, itera):
        self.iteraciones = int(itera)
        
    def setCerca(self, cerc):
        self.cerca = float(cerc)
        
    def setMedia(self, med):
        self.media = float(med)
        
    def setLejos(self, lej):
        self.lejos = float(lej)
        
    def setMaxPuntos(self, maxp):
        self.maxpuntos = int(maxp)
        
    def setMinPuntos(self, minp):
        self.minpuntos = int(minp)
        
    def setUmbral(self, umbr):
        self.umbraldistancia = float(umbr)
        
    def setCliente(self, cli):
        self.cliente = int(cli)

params = Parametros()
    

