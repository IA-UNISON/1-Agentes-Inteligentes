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
        self.x = x0[0]

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