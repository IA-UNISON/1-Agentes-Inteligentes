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
from random import choice, random
from copy import deepcopy

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos
    """
    def __init__(self, x0=[[0,0], [["sucio" for _ in range(3)] for _ in range(3)]]):
        self.x = deepcopy(x0)
        self.costo = 0

    def accion_legal(self, accion):
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
        if not self.accion_legal(accion):
            return 
        
        piso, cuarto = self.x[0]
        cuartos = deepcopy(self.x[1])
        if any("sucio" in piso_ for piso_ in self.x[1]):
            self.costo += 1
        if accion == "limpiar":
            self.costo += 1
            cuartos[piso][cuarto] = "limpio"
        elif accion == "ir_Derecha":
            self.costo += 2
            cuarto += 1
        elif accion == "ir_Izquierda":
            self.costo += 2
            cuarto -= 1
        elif accion == "subir":
            self.costo += 3
            piso += 1
        elif accion == "bajar":
            self.costo += 3
            piso -= 1

        self.x[0] = (piso, cuarto)
        self.x[1] = cuartos
    
    def percepcion(self):
        piso, cuarto = self.x[0]
        estado_actual = self.x[1][piso][cuarto]
        return (piso,cuarto), estado_actual


class NueveCuartosAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self,_):
        return choice(self.acciones)
    
class AgenteReactivoNueveCuartos(entornos_o.Agente):
    """
    
    Un agente reactivo en el modelos de los nueve cuartos

    """

    def __init__(self):
        """
   
        Inicializa en el peor de los casos (todos los cuartos sucios)

        """
        self.modelo = [(0,0), [["sucio" for _ in range(3)] for _ in range(3)]]
    
    def programa(self, percepcion):
        robot, situacion = percepcion
        piso, cuarto = robot

        self.modelo[0] = robot
        self.modelo[1][piso][cuarto] = situacion
        cuartos = self.modelo[1]

        if situacion == "sucio":
            return "limpiar"
        if piso == 0:
            return "subir" if cuarto == 2 else "ir_Derecha"
        elif piso == 1:
            if "sucio" in cuartos[1][0:cuarto]:
                return "ir_Izquierda"
            elif cuarto < 2:
                return "ir_Derecha"
            else:
                return "subir"
        elif piso == 2:
            return "ir_Izquierda" if cuarto > 0 else "nada"

class NueveCuartosCiego(NueveCuartos):
    """
    Igual a nueve cuartos solo que solo conoce el cuarto en el que esta pero no el estado del cuarto
    
    """
    def percepcion(self):
        return self.x[0]
    
class AgenteReactivoCiego(entornos_o.Agente):
    def __init__(self):
        """
   
        Inicializa suponiendo que estamos en el peor de los casos (todos los cuartos sucios)

        """
        self.modelo = [(0,0), [["sucio" for _ in range(3)] for _ in range(3)]]

    def programa(self, percepcion):
        robot = percepcion
        piso, cuarto = robot

        self.modelo[0] = robot
        cuartos = self.modelo[1]

        if self.modelo[1][piso][cuarto] == "sucio":
            self.modelo[1][piso][cuarto] = "limpio"
            return "limpiar"
        if piso == 0:
            return "subir" if cuarto == 2 else "ir_Derecha"
        elif piso == 1:
            if "sucio" in cuartos[1][0:cuarto]:
                return "ir_Izquierda"
            elif cuarto < 2:
                return "ir_Derecha"
            else:
                return "subir"
        elif piso == 2:
            return "ir_Izquierda" if cuarto > 0 else "nada"

class NueveCuartosEstocastico(NueveCuartos):
    """
    Variante de la clase nueve cuartos solo que ahora se le agrega cierta incertidumbre:
    80% de la veces que aspira intenta limpiar el cuarto lo hace con éxito.
    80% de las veces que inenta moverse se mueve con éxito.
    10% de las veces que intenta moverse se queda en el mismo cuarto.
    10% de las veces que intenta moverse escoge una acción legal al azar.
    
    """
    def transicion(self, accion):
        if not self.accion_legal(accion):
            return 
        
        piso, cuarto = self.x[0]
        cuartos = deepcopy(self.x[1])
        dado = random()

        if any("sucio" in piso_ for piso_ in self.x[1]):
            self.costo += 1
        if accion == "limpiar":
            self.costo += 1
            cuartos[piso][cuarto] = "limpio" if dado <= 0.8 else "sucio"
        elif accion in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]:
            self.costo += 3 if accion in ["subir", "bajar"] else 2
            if dado <= 0.8:
                piso, cuarto = self.resultado_movimiento(piso, cuarto, accion)
            elif dado < 9:
                pass
            else:
                acciones_posibles = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
                legales = [a for a in acciones_posibles if self.accion_legal(a) and a != accion]
                accion_accidental = choice(legales)

                if accion_accidental == "limpiar":
                    cuartos[piso][cuarto] = "limpio"
                else:
                    piso, cuarto = self.resutado_movimiento(piso, cuarto, accion_accidental)



        self.x[0] = (piso, cuarto)
        self.x[1] = cuartos
    
    def resultado_movimiento(self, piso, cuarto, accion):
        if accion == "ir_Derecha": return piso, cuarto + 1
        if accion == "ir_Izquierda": return piso, cuarto -1
        if accion == "subir": return piso + 1, cuarto
        if accion == "bajar": return piso - 1, cuarto
        return piso, cuarto 
        
        

def test():
    """
    Prueba de entornos y agentes, midiendo desempeño
    """

    x0 = [(0, 0), [["sucio" for _ in range(3)] for _ in range(3)]]
    acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    pruebas = [
        ("Aleatorio Normal", NueveCuartos(x0), NueveCuartosAleatorio(acciones)),
        ("Reactivo Normal", NueveCuartos(x0), AgenteReactivoNueveCuartos()),
        ("Aleatorio Ciego", NueveCuartosCiego(x0), NueveCuartosAleatorio(acciones)),
        ("Reactivo Ciego", NueveCuartosCiego(x0), AgenteReactivoCiego()),
        ("Aleatorio Estocástico", NueveCuartosEstocastico(x0), NueveCuartosAleatorio(acciones)),
        ("Reactivo Estocástico", NueveCuartosEstocastico(x0), AgenteReactivoNueveCuartos()),
    ]

    resultados = []

    for nombre, entorno, agente in pruebas:
        entornos_o.simulador(entorno, agente, 200)

        resultados.append((nombre, entorno.costo))

    print("\nResumen de Resultados:")
    print("-" * 30)
    for nombre, costo in resultados:
        print(f"Agente: {nombre:25s} | Costo total: {costo}")

if __name__ == "__main__":
    test()
