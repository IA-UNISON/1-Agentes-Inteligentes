#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'KarolBurrola'

import entornos_o
import  random
from random import choice

class NueveCuartos(entornos_o.Entorno):
    """

    Estructura base para los cuartos:
    P3: 6 -- 7 -- 8
    P2: 3 -- 4 -- 5
    P1: 0 -- 1 -- 2

    Reglas:
    - El robot debe de limpiar todos los cuartos
    - El robot inicia en la casilla 0 y solo puede moverse a la izquierda
    - El robot puede subir ÚNICAMENTE cuando está en el borde derecho, es decir, la columna que tiene el 8, 5 y 2 (Ej: Partiendo del 2 hacia arriba hasta llegar al 8)
    - El robot puede bajar ÚNICAMENTE cuando está en el borde izquierdo, es decir, la columna que tiene el 6, 3 y 0 (Ej: Partiendo del 6 hacia abajo donde puede llegar al 3)
    - El robot puede desplazarse tanto a la izquierda como hacia la derecha mientras esté en una casilla de en medio
    - El robot NO puede desplazarse a la izquierda si está en el borde izquierdo, es decir, la columna que tiene el 6, 3 y 0 (SOLO PUEDE A LA DERECHA)
    - El robot NO puede desplazarse a la derecha si está en el borde derecho, es decir, la columna que tiene el 8,5 y el 2 (SOLO PUEDE A LA IZQUIERDA)
    - El patrón a notar es que de izquierda a derecha se suma i+1 y de derecha a izquierda es i-1
    - Otro patrón a notar es que para subir es i+3, mientras que para bajar es i-3

    """
#Comenzamos con el robot en la casilla 0 y todos los cuartos sucios
    def __init__(self, x0=[0, "sucio", "sucio","sucio","sucio","sucio","sucio","sucio","sucio","sucio"]):
        self.x = x0[:]
        self.costo=0

#Corrobora si la acción que se está realizando es posible de hacerse o no
    def accion_legal(self, accion):
        robot = self.x[0]

        if accion == "ir_Derecha":
            return robot not in [2,5,8]
        if accion == "ir_Izquierda":
            return robot not in [0,3,6]
        if accion == "subir":
            return robot == 2 or robot == 5
        if accion == "bajar":
            return robot == 6 or robot == 3

        return True #Por si llega a ser la opción "limpiar" o "nada", esto es válido

    def transicion(self,accion):

        """
        Costos de las acciones:
        Nada = 0
        Limpiar = 1
        Ir a la derecha/izquierda = 2
        Subir/Bajar = 3
        """

        robot = self.x[0]
        costopaccion = 0

        if accion == "limpiar":
            costopaccion = 1
        elif accion in ("ir_Derecha", "ir_Izquierda"):
            costopaccion = 2
        elif accion in ("subir", "bajar"):
            costopaccion = 3

        self.costo += costopaccion
        if not self.accion_legal(accion):
            return
        if accion == "limpiar":
            self.x[robot+1] = "limpio"
        elif accion == "ir_Izquierda":
            self.x[0] -= 1
        elif accion == "ir_Derecha":
            self.x[0] += 1
        elif accion == "subir":
            self.x[0] += 3
        elif accion == "bajar":
            self.x[0] -= 3

    def percepcion(self):
            robot = self.x[0]
            return self.x[0], self.x[robot+1]

class AgenteAleatorio(entornos_o.Agente):
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)

class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    def __init__(self):
        self.modelo = [0, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]

    def programa(self, percepcion):
        robot, situacion = percepcion
        self.modelo[0] = robot
        self.modelo[robot + 1] = situacion

        #Si todos los cuartos están limpios, se detiene
        if all(habitacion == "limpio" for habitacion in self.modelo[1:]):
            return "nada"
        #Si el lugar actual está sucio, se limpia
        if situacion == "sucio":
            return "limpiar"

        """
        Mi estrategia consiste en lo siguiente:
        
        """
        if robot == 0 or robot == 1:
            return "ir_Derecha"
        elif robot == 2:
            return "subir"
        elif robot == 5:
            return "subir"
        elif robot == 8 or robot == 7:
            return "ir_Izquierda"
        elif robot == 6:
            return "bajar"
        elif robot == 3:
            return "ir_Derecha"
        elif robot == 4:
            return "nada"

        return "nada"

class NueveCuartosCiego(NueveCuartos):
    def percepcion(self):
        return self.x[0]

class AgenteReactivoModeloNueveCuartosCiego(AgenteReactivoModeloNueveCuartos):
    def programa(self, percepcion):
        robot = percepcion
        self.modelo[0] = robot

        if all(habitacion == "limpio" for habitacion in self.modelo[1:]):
            return "nada"

        hip = self.modelo[robot + 1]
        if hip == "sucio":
            self.modelo[robot+1] = "limpio"
            return "limpiar"

        if robot == 0 or robot == 1:
            return "ir_Derecha"
        elif robot == 2:
            return "subir"
        elif robot == 5:
            return "subir"
        elif robot == 8 or robot == 7:
            return "ir_Izquierda"
        elif robot == 6:
            return "bajar"
        elif robot == 3:
            return "ir_Derecha"
        elif robot == 4:
            return "nada"

        return "nada"

class NueveCuartosEstocastico(NueveCuartos):
        def transicion(self, accion):
            robot = self.x[0]
            costopaccion = 0
            if accion == "limpiar":
                costopaccion = 1
            elif accion in ["ir_Derecha", "ir_Izquierda"]:
                costopaccion = 2
            elif accion in ["subir", "bajar"]:
                costopaccion = 3

            self.costo += costopaccion
            if not self.accion_legal(accion):
                return
            rand = random.random()
            if accion == "limpiar":
                if rand <= 0.8:
                    self.x[robot+1] = "limpio"
            else:
                if rand <= 0.8:
                    res = accion
                elif rand <= 0.9:
                    return
                else:
                    movs = ["subir", "bajar", "ir_Derecha", "ir_Izquierda"]
                    prob = [x for x in movs if self.accion_legal(x)]
                    res = random.choice(prob)
                    if res == "ir_Izquierda":
                        self.x[0] -= 1
                    elif res == "ir_Derecha":
                        self.x[0] += 1
                    elif res == "subir":
                        self.x[0] += 3
                    elif res == "bajar":
                        self.x[0] -= 3

class AgenteReactivoModeloEstocastico(AgenteReactivoModeloNueveCuartos):
    pass

def test():

    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(), AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]), 200)

    print("Prueba del entorno con un agente reactivo modelo")
    entornos_o.simulador(NueveCuartos(), AgenteReactivoModeloNueveCuartos(), 200)

    print("Prueba del entorno NueveCuartosCiego con un agente reactivo con modelo ciego")
    entornos_o.simulador(NueveCuartosCiego(), AgenteReactivoModeloNueveCuartosCiego(), 200)

    print("Prueba del entorno NuveCuartosEstocastico con agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosEstocastico(), AgenteReactivoModeloEstocastico(), 200)

if __name__ == "__main__":
    test()
