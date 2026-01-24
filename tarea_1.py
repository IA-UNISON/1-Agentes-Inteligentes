#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Rogelio Peralta'

import entornos_f
import entornos_o
from random import choice

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos
    """
    def __init__(self, x0=[[0,0], [["sucio" for _ in range(3)] for _ in range(3)]]):
        self.x = x0
        self.costo = 0

    def acción_legal(self, accion):
        piso , cuarto = self.x[0]
        if accion == "ir_Izquierda":
            return cuarto > 0 
        if accion == "ir_Derecha":
            return cuarto < 2
        if accion == "subir":
            return piso < 2 and cuarto == 2
        if accion == "bajar":
            return piso > 0 and cuarto == 0
        return accion in ("limpiar", "nada")
    
    def transicion(self, accion):
        if not self.acción_legal(accion):
            return 
        
        robot, cuartos = self.x[0], self.x[1]
        if any("sucio" in piso for piso in cuartos):
            self.costo += 1
        if accion == "limpiar":
            self.costo += 1
            cuartos[robot[0]][robot[1]] = "limpio"
        elif accion == "ir_Derecha":
            self.costo += 2
            robot[1] += 1
        elif accion == "ir_Izquierda":
            self.costo += 2
            robot[1] -= 1
        elif accion == "subir":
            self.costo += 3
            robot[0] += 1
        elif accion == "bajar":
            self.costo += 3
            robot[0] -= 1

    def percepcion(self):
        robot = self.x[0]
        return robot, self.x[1][robot[0]][robot[1]]


class NueveCuartosAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self,_):
        return choice(self.acciones)

def test():
    """
    Prueba de entornos y agentes, midiendo desempeño
    """

if __name__ == "__main__":
    test()
