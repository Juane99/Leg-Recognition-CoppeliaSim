#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Juan Emilio Martinez Manjon
Asignatura: Programacion Tecnica y Cientifica
Profesor: Eugenio Aguirre Molina
Curso: 2020/2021
"""

# clasificarSVM.py

"""
Este fichero utiliza diferentes kernels para encontrar el mejor clasificador
SVM para nuestro problema. Para ello usaremos GridSearchCV para obtener
los mejores hiperparámetros de cada kernel, y 5-fold CV para obtener la
accuracy de cada uno. Nos quedaremos con el modelo que obtenga mejor
Cross-Validation y lo guardaremos en un archivo pkl.
"""

import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
import pickle

# import warnings filter
from warnings import simplefilter


def main():
    
    #Inicializamos el mejor clasificador y lo vamos actualizando en 
    #funcion del CV-5fold accuracy
    mejor_accuracy = 0
    

    # ignore all future warnings
    simplefilter(action='ignore', category=FutureWarning)
    simplefilter(action='ignore', category=DeprecationWarning)
    
    # Assign colum names to the dataset
    colnames = ["perimetro", "profundidad", "anchura", "esPierna"]
    
    # cargamos los datos
    # Read dataset to pandas dataframe
    piernasdata = pd.read_csv("piernasDataset.csv", names=colnames) 
    
    # Separamos las características de la etiqueta que nos dices a la clase que corresponde
    X = piernasdata.drop('esPierna', axis=1)  
    y = piernasdata['esPierna']  
    
    
    '''
    Dividimos en conjunto de entrenamiento y de prueba de forma aleatoria
    con random_state fijamos la semilla del generador aleatorio para que no
    vayan cambiando los resultados entre una ejecución y otra
    '''
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=25)
    
    
    #Vamos a probar con los kernel lineal, polinómico y radial para ver
    #cual nos da mejores resultados.
    
    '''
    KERNEL LINEAL
    '''
    
    print("###################################")
    print("# Clasificación con kernek Lineal #")
    print("###################################")

    svcLineal = SVC(kernel='linear')  
    svcLineal.fit(X_train, y_train)
    
    
    # Con el clasificador obtenido hacemos la predicción sobre el conjunto de test incial
    
    y_pred = svcLineal.predict(X_test)
    
    acc_test=accuracy_score(y_test, y_pred)
    
    print("Acc_test Lineal: (TP+TN)/(T+P)  %0.4f" % acc_test)
    
    print("Matriz de confusión Filas: verdad Columnas: predicción")
   
    print(confusion_matrix(y_test, y_pred))
       
    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))
    
    #Para asegurarnos de que el resultado no depende del conjunto de test elegido
    #tenemos que realizar validación cruzada. Antes vamos a buscar los mejores
    #hiperparámetros para este kernel lineal. Después aplicaremos la validación
    #cruzada al modelo con los mejores hiperparámetros
    
    
    param_grid={'C':[1,10,100,1000],
                'shrinking':[True,False]}
    
    clf=GridSearchCV(SVC(kernel='linear'), param_grid, n_jobs=-1)
    clf.fit(X_train,y_train)
    
    print("\nMejores Hiperparámetros Kernel lineal:",clf.best_params_)
    
    svcLineal2 = SVC(kernel='linear',C=1, shrinking=True)
    
    scores = cross_val_score(svcLineal2, X_train, y_train, cv=5)
    
    # exactitud media con intervalo de confianza del 95%
    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))
   
    
    #Miramos si la accuray es mejor que la mejor actual
    
    if (scores.mean() > mejor_accuracy):
        mejor_accuracy = scores.mean()
        mejor_clasificador = svcLineal2
        mejor_clasificador_str = "El mejor clasificador es el SVC con kernel Lineal"
    
    #Ahora evaluamos sobre el conjunto de test y sacamos su correspondiente
    #matriz de confusion
    
    svcLineal2.fit(X_train,y_train)
    y_pred = svcLineal2.predict(X_test)
    
    acc_test=accuracy_score(y_test, y_pred)
    
    print("Acc_test Lineal2: (TP+TN)/(T+P)  %0.4f" % acc_test)
    
    print("Matriz de confusión Filas: verdad Columnas: predicción")
    
    print(confusion_matrix(y_test, y_pred))
    
    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))   
    
    print('\n\n')
    
    '''
    KERNEL POLINOMICO
    '''
    
    print("#######################################")
    print("# Clasificación con kernek polinomico #")
    print("#######################################")
    
    #Para la evaluación inicial usaremos grado 3, pero después usaremos
    #un Grid de hiperparámetros para estimar el mejor de todos ellos
    
    svcPol = SVC(kernel='poly', degree=3)  
    svcPol.fit(X_train, y_train)
    
    
    # Con el clasificador obtenido hacemos la predicción sobre el conjunto de test incial
    
    y_pred = svcPol.predict(X_test)
    
    acc_test=accuracy_score(y_test, y_pred)
    
    print("Acc_test Polinomico: (TP+TN)/(T+P)  %0.4f" % acc_test)
    
    print("Matriz de confusión Filas: verdad Columnas: predicción")
    
    print(confusion_matrix(y_test, y_pred))
    
    
    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))
    
    #Para asegurarnos de que el resultado no depende del conjunto de test elegido
    #tenemos que realizar validación cruzada. Usamos un GridSearchCV también,
    #como hemos hecho para el kernel lineal
    
    
    param_grid={'C':[1,10,100,1000],
                'shrinking':[True,False],
                'degree':[3,4],
                'gamma':[0.001, 0.005, 0.01, 0.1]}
    
    clf=GridSearchCV(SVC(kernel='poly'), param_grid, n_jobs=-1)
    clf.fit(X_train,y_train)
    
    print("\nMejores Hiperparámetros Kernel Polinomico:",clf.best_params_)    
    
    svcPol2 = SVC(kernel='poly', degree=3, C=1, gamma=0.001, shrinking=True)
    
    scores = cross_val_score(svcPol2, X_train, y_train, cv=5)
    
    # exactitud media con intervalo de confianza del 95%
    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))
    
    
    #Miramos si la accuray es mejor que la mejor actual
    
    if (scores.mean() > mejor_accuracy):
        mejor_accuracy = scores.mean()
        mejor_clasificador = svcPol2
        mejor_clasificador_str = "El mejor clasificador es el SVC con kernel Polinomico"
    
    #Ahora evaluamos sobre el conjunto de test y sacamos su correspondiente
    #matriz de confusion
    
    svcPol2.fit(X_train,y_train)
    y_pred = svcPol2.predict(X_test)
    
    acc_test=accuracy_score(y_test, y_pred)
    
    print("Acc_test Poli2: (TP+TN)/(T+P)  %0.4f" % acc_test)
    
    print("Matriz de confusión Filas: verdad Columnas: predicción")
    
    print(confusion_matrix(y_test, y_pred))
    
    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))       
    
    print('\n\n')
    
    '''
    KERNEL RADIAL
    '''
    
    print("###########################################")
    print("# Clasificación con kernek de base radial #")
    print("###########################################")

    
    svcRBF = SVC(kernel='rbf', gamma='auto')  
    svcRBF.fit(X_train, y_train)
    
    
    # Con el clasificador obtenido hacemos la predicción sobre el conjunto de test incial
    
    y_pred = svcRBF.predict(X_test)
    
    acc_test=accuracy_score(y_test, y_pred)
    
    print("Acc_test RBF: (TP+TN)/(T+P)  %0.4f" % acc_test)
    
    print("Matriz de confusión Filas: verdad Columnas: predicción")
    
    print(confusion_matrix(y_test, y_pred))
        
    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))
    
    #Para asegurarnos de que el resultado no depende del conjunto de test elegido
    #tenemos que realizar validación cruzada. Usamos un GridSearchCV también,
    #como hemos hecho para el kernel lineal
    
    
    param_grid={'C':[1,10,100,1000],
                'shrinking':[True,False],
                'gamma':[0.001, 0.005, 0.01, 0.1]}
    
    clf=GridSearchCV(SVC(kernel='rbf'), param_grid, n_jobs=-1)
    clf.fit(X_train,y_train)
    
    print("\nMejores Hiperparámetros Kernel Radial:",clf.best_params_)  
    
    
    #realizando validación cruzada 5-cross validation, si hay 150 muestras
    #entonces está usandos 30 muestras de ejemplo cada vez y eso lo realiza 5 veces
    
    svcRBF2 = SVC(kernel='rbf', C=1000, gamma=0.1, shrinking=True)
    
    scores = cross_val_score(svcRBF2, X_train, y_train, cv=5)
    
    # exactitud media con intervalo de confianza del 95%
    print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))
  
    
    #Miramos si la accuray es mejor que la mejor actual
    
    if (scores.mean() > mejor_accuracy):
        mejor_accuracy = scores.mean()
        mejor_clasificador = svcRBF2
        mejor_clasificador_str = "El mejor clasificador es el SVC con kernel Radial"  
    
    #Ahora evaluamos sobre el conjunto de test y sacamos su correspondiente
    #matriz de confusion
    
    svcRBF2.fit(X_train,y_train)
    y_pred = svcRBF2.predict(X_test)
    
    acc_test=accuracy_score(y_test, y_pred)
    
    print("Acc_test Radial2: (TP+TN)/(T+P)  %0.4f" % acc_test)
    
    print("Matriz de confusión Filas: verdad Columnas: predicción")
    
    print(confusion_matrix(y_test, y_pred))
    
    print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
    print("f1-score es la media entre precisión y recall")
    print(classification_report(y_test, y_pred))       
    
    
    #GUARDAMOS EL MEJOR CLASIFICADOR EN UN FICHERO PKL
    
    print("Salvamos el mejor clasificador a disco, fichero clasificador.pkl")
    
    print("\n"+mejor_clasificador_str+"\n")
    
    # Guardamos el clasificador
    with open("clasificador.pkl", "wb") as archivo:
        pickle.dump(mejor_clasificador, archivo)
        