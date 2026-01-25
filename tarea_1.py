#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'andresgutierrez'

import entornos_o

class NueveCuartos(entornos_o.Entorno):
    def __init__(self, x0=[1, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        # Por default, el robot se encuentra en el primer cuarto y todos los cuartos estan sucios.
        self.x = x0[:]
        self.costo = 0

    def accion_legal(self, accion):
        robot = self.x[0]

        if accion in ("limpiar", "nada"):
            return True
        
        if accion == "ir_Derecha":
            return robot % 3 != 0
        
        if accion == "ir_Izquierda":
            return robot % 3 != 1
        
        if accion == "subir":
            return robot in (3, 6)
        
        if accion == "bajar":
            return robot in (4, 7)
        
        return False
    
    def transicion(self, accion):
        if not self.accion_legal(accion):
            return
        
        robot = self.x[0]

        if accion == "limpiar":
            self.costo += 1
        elif accion in ("ir_Derecha", "ir_Izquierda"):
            self.costo += 2
        elif accion in ("subir", "bajar"):
            self.costo += 5
        elif accion == "nada" and "sucio" in self.x[1:]:
            self.costo += 1

        if accion == "limpiar":
            self.x[robot] = "limpio"
        elif accion == "ir_Derecha":
            self.x[0] += 1
        elif accion == "ir_Izquierda":
            self.x[0] -= 1
        elif accion == "subir":
            self.x[0] += 3
        elif accion == "bajar":
            self.x[0] -= 3

    def percepcion(self):
        return self.x[0], self.x[self.x[0]]