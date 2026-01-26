#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Diego Gallegos Hernandez'

import entornos_o
import random

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos en una cuadricula 3x3.

    El estado se define como: (robot, 0, 1, 2, ..., 8) 
    donde robot puede tener los valores "0", "1", ....
    y los cuartos representados por numeros pueden ser "limpio" o "sucio"
    
    Las acciones validas en el entorno son
    ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    Donde subir solo es posible en los cuartos de la derecha, en los 
    primeros dos pisos, y bajar solo en los cuartos de la izquierda, en
    los dos ultimos pisos.
    Ir a la derecha y a la izquierda no son legales en todos los casos.
    
    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    
    def __init__(self, x0 = [0, "sucio", "sucio", "sucio", 
                                "sucio", "sucio", "sucio", 
                                "sucio", "sucio", "sucio",]):
        """
        El robot por default comienza en 0 y 
        todos los cuartos estan sucios.
        """
        self.x = x0[:]
        self.costo = 0
    
    def accion_legal(self, accion):
        """
        ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
        """
        if accion == "subir":
            return True if self.x[0] in (2, 5) else False
        elif accion == "bajar":
            return True if self.x[0] in (6, 3) else False
        elif accion == "ir_Derecha":
            return True if self.x[0] not in (2, 5, 8) else False
        elif accion == "ir_Izquierda":
            return True if self.x[0] not in (0, 3, 6) else False
        
        return accion in ("limpiar", "nada")
        
    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")
        
        nuevo_estado = self.x[:]
        robot = nuevo_estado[0]
        
        if accion == "ir_Derecha":
            robot += 1
            nuevo_estado[0] = robot
            self.costo += 2
        elif accion == "ir_Izquierda":
            robot -= 1
            nuevo_estado[0] = robot
            self.costo += 2
        elif accion == "subir":
            robot += 3
            nuevo_estado[0] = robot
            self.costo += 3
        elif accion == "bajar":
            robot -= 3
            nuevo_estado[0] = robot
            self.costo += 3
        elif accion == "limpiar":
            cuarto = robot
            nuevo_estado[cuarto + 1] = "limpio"
            self.costo += 1
        elif accion == "nada":
            self.costo += 0
        
        self.x = nuevo_estado
    
    def percepcion(self):
        robot = self.x[0]
        estado = self.x[robot + 1]
        return robot, estado
    
class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo. Conserva memoria de su entorno.
    """
    
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = [0, "sucio", "sucio", "sucio", 
                          "sucio", "sucio", "sucio", 
                          "sucio", "sucio", "sucio",]
        
    def programa(self, percepcion):
        robot, situacion = percepcion 
    
        self.modelo[0] = robot
        self.modelo[robot + 1] = situacion
    
        if situacion == "sucio":
            return "limpiar"
    
        objetivo = None
        for i, estado in enumerate(self.modelo[1:]):
            if estado == "sucio":
                objetivo = i
                break

        if objetivo is not None and objetivo > robot:
            if robot in (2, 5):
                return "subir"
            else: 
                return "ir_Derecha"

        if objetivo is not None and objetivo < robot:
            if robot in (6, 3):
                return "bajar"
            else:
                return "ir_Izquierda"
        
        if all(cuarto == "limpio" for cuarto in self.modelo[1:]):
            return "nada"
    
        # exploración
        if robot in (2, 5):
            return random.choice(["ir_Izquierda", "subir"])
        elif robot in (6, 3):
            return random.choice(["ir_Derecha", "bajar"])
        elif robot in (1, 4, 7): 
            return random.choice(["ir_Derecha", "ir_Izquierda"])
        elif robot == 0:
            return "ir_Derecha"
        elif robot == 8:
            return "ir_Izquierda"

        return "nada"
