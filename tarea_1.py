#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Javier Leonardo Miranda Sánchez'

import entornos_f
import entornos_o

from random import *

import entornos_o
from random import choice, random


class NueveCuartos(entornos_o.Entorno):
    """
    Entorno de nueve cuartos (3 pisos x 3 cuartos)

    Estado:
    [piso, cuarto, c00, c01, c02, c10, c11, c12, c20, c21, c22]
    """

    def __init__(self):
        self.x = [0, 0] + ["sucio"] * 9
        self.costo = 0

    def accion_legal(self, accion):
        piso, cuarto = self.x[0], self.x[1]

        if accion in ("ir_Derecha", "ir_Izquierda", "limpiar", "nada"):
            return True
        if accion == "subir":
            return piso < 2 and cuarto == 2
        if accion == "bajar":
            return piso > 0 and cuarto == 0
        return False

    def transicion(self, accion):
        if not self.accion_legal(accion):
            return

        piso, cuarto = self.x[0], self.x[1]
        idx = 2 + piso * 3 + cuarto

        if accion == "limpiar":
            self.x[idx] = "limpio"
            self.costo += 1

        elif accion == "ir_Derecha" and cuarto < 2:
            self.x[1] += 1
            self.costo += 2

        elif accion == "ir_Izquierda" and cuarto > 0:
            self.x[1] -= 1
            self.costo += 2

        elif accion == "subir":
            self.x[0] += 1
            self.costo += 4

        elif accion == "bajar":
            self.x[0] -= 1
            self.costo += 4

    def percepcion(self):
        piso, cuarto = self.x[0], self.x[1]
        estado = self.x[2 + piso * 3 + cuarto]
        return piso, cuarto, estado

class AgenteAleatorio(entornos_o.Agente):

    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)

class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):

    def __init__(self):
        self.modelo = [0, 0] + ["sucio"] * 9

    def programa(self, percepcion):
        piso, cuarto, estado = percepcion
        self.modelo[0] = piso
        self.modelo[1] = cuarto
        self.modelo[2 + piso * 3 + cuarto] = estado

        if estado == "sucio":
            return "limpiar"

        # Busca algún cuarto sucio en el modelo
        for p in range(3):
            for c in range(3):
                if self.modelo[2 + p * 3 + c] == "sucio":
                    if p > piso:
                        return "subir"
                    if p < piso:
                        return "bajar"
                    if c > cuarto:
                        return "ir_Derecha"
                    if c < cuarto:
                        return "ir_Izquierda"

        return "nada"

class NueveCuartosCiego(NueveCuartos):

    def percepcion(self):
        return self.x[0], self.x[1]

class AgenteModeloNueveCuartosCiego(entornos_o.Agente):

    def __init__(self):
        self.modelo = [0, 0] + ["sucio"] * 9

    def programa(self, percepcion):
        piso, cuarto = percepcion
        self.modelo[0] = piso
        self.modelo[1] = cuarto

        idx = 2 + piso * 3 + cuarto
        if self.modelo[idx] == "sucio":
            self.modelo[idx] = "limpio"
            return "limpiar"

        return choice(["ir_Derecha", "ir_Izquierda", "subir", "bajar"])

class NueveCuartosEstocastico(NueveCuartos):

    def transicion(self, accion):

        r = random()

        if accion == "limpiar":
            if r < 0.8:
                super().transicion("limpiar")
            else:
                self.costo += 1

        else:
            if r < 0.8:
                super().transicion(accion)
            elif r < 0.9:
                self.costo += 1
            else:
                super().transicion(choice(
                    ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "nada"]
                ))

def test():
    acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    print("Agente aleatorio")
    entornos_o.simulador(NueveCuartos(),
                         AgenteAleatorio(acciones),
                         200)

    print("Agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(),
                         AgenteReactivoModeloNueveCuartos(),
                         200)

    print("Entorno ciego")
    entornos_o.simulador(NueveCuartosCiego(),
                         AgenteModeloNueveCuartosCiego(),
                         200)

    print("Entorno estocástico")
    entornos_o.simulador(NueveCuartosEstocastico(),
                         AgenteReactivoModeloNueveCuartos(),
                         200)


if __name__ == "__main__":
    test()


# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

