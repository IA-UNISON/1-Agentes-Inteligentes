#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'KarolBurrola'

import entornos_f
import entornos_o
import  random
from random import choice

class NueveCuartos(entornos_o.Entorno):
    def __init__(self, x0=[0, "sucio", "sucio","sucio","sucio","sucio","sucio","sucio","sucio","sucio"]):
        self.x = x0[:]
        self.costo=0

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

        return True

    def transicion(self,accion):
        robot = self.x[0]
        costopaccion = 0

        if accion == "limpiar":
            costopaccion = 1
        elif accion in ("ir_Derecha", "ir_Izquierda"):
            costopaccion = 2
        elif accion in ("subir", "bajar"):
            costopaccion = 3
        else:
            raise ValueError("Accion no valida")

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

        if all(habitacion == 'limpio' for habitacion in self.modelo[1:]):
            return 'nada'
        if situacion == 'sucio':
            return 'limpiar'

        if robot == 0 or robot == 1:
            return 'ir_Derecha'
        elif robot == 2:
            return 'subir'
        elif robot == 5:
            return 'subir'
        elif robot == 8 or robot == 7:
            return 'ir_Izquierda'
        elif robot == 6:
            return 'bajar'
        elif robot == 3:
            return 'ir_Derecha'
        elif robot == 4:
            return 'nada'

        return 'nada'
















# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python