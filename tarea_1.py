#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

import entornos_o
from random import choice

class NueveCuartos(entornos_o.Entorno):
    def __init__(self):
       
       self.x = [
            0,  # piso inicial
            0,  # cuarto inicial
            [ ["sucio" for _ in range(3)] for _ in range(3) ]  # matriz 3x3 independiente
        ]
       
       self.costo = 0
       
    """self.x = [
            0,                                  # piso inicial
            0,                                  # cuarto inicial
            [
                ["sucio", "sucio", "sucio"],    # piso 0
                ["sucio", "sucio", "sucio"],    # piso 1
                ["sucio", "sucio", "sucio"]     # piso 2
            ]
        ]
        self.x[0] -> piso actual (0,1,2)
        self.x[1] -> cuarto actual (0,1,2)
        self.x[2] -> matriz 3x3 con estado de cada cuarto ("sucio"/"limpio")
        """
        

    def accion_legal(self, accion):
        piso, cuarto, _ = self.x
        acciones = ["limpiar", "nada"]

        # movimiento horizontal
        if cuarto > 0:
            acciones.append("ir_Izquierda")
        if cuarto < 2:
            acciones.append("ir_Derecha")

        # movimiento vertical
        if piso < 2 and cuarto == 2:  # solo cuarto derecho puede subir
            acciones.append("subir")
        if piso > 0 and cuarto == 0:  # solo cuarto izquierdo puede bajar
            acciones.append("bajar")

        return accion in acciones
    
    def transicion(self, accion):
        if not self.accion_legal(accion):
            print(f"Acción ilegal: {accion}")
            return
        
        piso = self.x[0]
        cuarto = self.x[1]

        costos = {"limpiar": 1,"ir_Derecha": 2,"ir_Izquierda": 2,"subir": 3,"bajar": 3,"nada": 0}
        self.costo += costos.get(accion, 1)

        # Ejecutar acción
        if accion == "limpiar":
            self.x[2][piso][cuarto] = "limpio"
        elif accion == "ir_Derecha":
            self.x[1] += 1
        elif accion == "ir_Izquierda":
            self.x[1] -= 1
        elif accion == "subir":
            self.x[0] += 1
        elif accion == "bajar":
            self.x[0] -= 1
        
        print(f"[DEBUG] Acción: {accion}, Piso: {self.x[0]}, Cuarto: {self.x[1]}, Estado: {self.x[2]}")

    """def transicion(self, accion):
        if not self.accion_legal(accion):
            return
        
        piso = self.x[0]
        cuarto = self.x[1]
        # piso, cuarto, cuartos = self.x

        costos = {
            "limpiar": 1,
            "ir_Derecha": 2,
            "ir_Izquierda": 2,
            "subir": 3,
            "bajar": 3,
            "nada": 0
            }
        self.costo += costos.get(accion, 1)  # 1 por defecto
        

        # Ejecutar acción
        if accion == "limpiar":
            self.x[2][piso][cuarto] = "limpio"
        elif accion == "ir_Derecha":
            self.x[1] += 1
        elif accion == "ir_Izquierda":
            self.x[1] -= 1
        elif accion == "subir":
            self.x[0] += 1
        elif accion == "bajar":
            self.x[0] -= 1
        # 'nada' no hace nada
        """

    def percepcion(self):
        piso = self.x[0]
        cuarto = self.x[1]
        estado = self.x[2][piso][cuarto]  # el estado del cuarto actual
        return (piso, cuarto), estado
        

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que elige al azar entre las acciones legales del entorno
    """
    def programa(self, percepcion, entorno=None):
        # Si se pasa el objeto entorno, obtenemos las acciones legales dinámicamente
        acciones_legales = [a for a in ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
                            if entorno.accion_legal(a)] if entorno else ["limpiar","nada","ir_Derecha","ir_Izquierda","subir","bajar"]
        return choice(acciones_legales)
    

class AgenteReactivoNueveCuartos(entornos_o.Agente):
    """
    Agente reactivo simple para el entorno de 3x3
    """
    def programa(self, percepcion):
        (piso, cuarto), estado = percepcion

        # Limpia si el cuarto está sucio
        if estado == "sucio":
            return "limpiar"

        # Si está limpio, decide moverse
        # Estrategia simple: ir a la derecha hasta el final,
        # luego bajar o subir según legalidad
        if cuarto < 2:
            return "ir_Derecha"
        elif cuarto == 2 and piso < 2:
            return "subir"
        elif cuarto > 0:
            return "ir_Izquierda"
        elif cuarto == 0 and piso > 0:
            return "bajar"
        else:
            return "nada"



def test():
    """
    Prueba del entorno NueveCuartos y los agentes
    """
    
    print("Prueba del entorno con un agente aleatorio")
    agente_aleatorio = AgenteAleatorio()
    entorno = NueveCuartos()
    entornos_o.simulador(entorno,
                         agente_aleatorio,
                         pasos=200)
    
    print("Prueba del entorno con un agente reactivo simple")
    agente_reactivo = AgenteReactivoNueveCuartos()
    entorno2 = NueveCuartos()
    entornos_o.simulador(entorno2,
                         agente_reactivo,
                         pasos=200)

    """print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartos(x0), 
                         AgenteReactivoModeloDosCuartos(), 
                         100)

    print("Prueba del entorno ciego con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosCiego(x0), 
                         AgenteReactivoModeloDosCuartosCiego(), 
                         100)"""


if __name__ == "__main__":
    test()
