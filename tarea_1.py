#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'escribe_tu_nombre'

import entornos_f
import entornos_o

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

import entornos_f
from random import choice
from random import random 


class NueveCuartos(entornos_f.Entorno):
    """
    Clase para un entorno de nueve cuartos.
    Muy sencilla solo regrupa métodos.

    El estado se define como (robot, 
                                A, B, C, 
                                D, E, F, 
                                G, H, I)
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F", "G", "H", "I"
    A, B, C, D, E, F, G, H y I pueden tener los valores "limpio", "sucio"

    A, D, G son los cuartos más a la izquierda, Solo en estos se puede bajar
    C, F, I son los cuartos más a la derecha, Solo en estos se puede subir

    A, B, C Son el primer piso, en este no se puede bajar
    D, E, F Son el segundo piso, en este se puede bajar o subir
    G, H, I Son el tercer piso, en este solo se puede bajar

    Las acciones válidas en el entorno son
        ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def accion_legal(self, _, accion):
        return accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")

    def transicion(self, estado, acción):

        DERECHA = {"A":"B","B":"C","D":"E","E":"F","G":"H","H":"I"}
        IZQUIERDA = {v:k for k,v in DERECHA.items()}
        #genera un diccionario donde las transiciones estan invertidas por lo tanto 
        #ahora el primer elemento es "B":"A"

        SUBIR = {"C":"F","F":"I"}
        #Son las trancisiones donde es valido subir y a donde llegas

        BAJAR = {"G": "D", "D": "A"}
        #Son las trancisiones donde es valido bajar y a donde llegas

        robot = estado[0]
        cuartos = list(estado[1:])

        c_local = 2

        if acción == "ir_Derecha" and robot in DERECHA:
            robot = DERECHA[robot]

        elif acción == "ir_Izquierda" and robot in IZQUIERDA:
            robot = IZQUIERDA[robot]

        elif acción == "subir" and robot in SUBIR:
            robot = SUBIR[robot]
            c_local = 3

        elif acción == "bajar" and robot in BAJAR:
            robot = BAJAR[robot]
            c_local = 3

        elif acción == "limpiar":
            idx = "ABCDEFGHI".index(robot)
            cuartos[idx] = "limpio"
            c_local = 1

        elif acción == "nada":
            c_local = 0

        return (tuple([robot] + cuartos), c_local)




    def percepcion(self, estado):
        robot = estado[0]
        idx = "ABCDEFGHI".index(robot)
        return robot, estado[idx + 1]
    
    

class AgenteAleatorio(entornos_f.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)


class AgenteReactivoModeloNuevecuartos(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo, donde el agente solo percive su ubicación

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ["A",
        "sucio", "sucio", "sucio",
        "sucio", "sucio", "sucio",
        "sucio", "sucio", "sucio"]

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        idx = "ABCDEFGHI".index(robot)
        self.modelo[idx + 1] = situación

        #self.modelo[1:4] - primer piso
        #self.modelo[4:7] - segundo piso
        #self.modelo[7:10] - tercer piso

        #Cuando todos los pisos estan limpios no hace nada
        if all(x == "limpio" for x in self.modelo[1:]):
            return "nada"

        if situación == "sucio":
            return "limpiar"

        # si esta todo el primer esta piso limpio ir al segundo
        if robot == "C" and all(x == "limpio" for x in self.modelo[1:4]):
            return "subir"

        # si esta todo el segundo esta piso limpio ir al tercer
        if robot == "F" and all(x == "limpio" for x in self.modelo[4:7]):
            return "subir"

        # si esta todo el tercer esta piso limpio ir abajo
        #if robot == "G" and all(x == "limpio" for x in self.modelo[7:10]):
        #   return "bajar"
        
        # si esta todo el segundo esta piso limpio ir abajo
        #if robot == "D" and all(x == "limpio" for x in self.modelo[4:7]):
        #    return "bajar"
        
        #el modelo en los cuartos del centro determina cual cuarto ya limpie? para ir al contrario
        if robot == "B":
            return "ir_Izquierda" if self.modelo[1] == "sucio" else "ir_Derecha"

        if robot == "E":
            return "ir_Izquierda" if self.modelo[4] == "sucio" else "ir_Derecha"

        if robot == "H":
            return "ir_Izquierda" if self.modelo[7] == "sucio" else "ir_Derecha"

        #Movimientos basicos
        if robot in ("A", "D", "G"):
            return "ir_Derecha"

        if robot in ("C", "F", "I"):
            return "ir_Izquierda"
        
        return "nada"
    

class AgenteReactivoModeloNueveCuartosCiego(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo

    """

    def percepción(self, estado):
        return (estado[0],)

    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ["A",
        "sucio", "sucio", "sucio",
        "sucio", "sucio", "sucio",
        "sucio", "sucio", "sucio"]

    def programa(self, percepción):
        robot = percepción[0]

        # Actualiza el modelo interno
        self.modelo[0] = robot
        idx = "ABCDEFGHI".index(robot)

        #actualizamos internamente el estado del robot
        if self.modelo[idx + 1] == "sucio":
            self.modelo[idx + 1] = "limpio"
            return "limpiar"
        
        if all(x == "limpio" for x in self.modelo[1:]):
            return "nada"

        if robot in ("A", "B"):
            return "ir_Derecha"
        if robot == "C":
            return "subir"

        if robot in ("D", "E"):
            return "ir_Derecha"
        if robot == "F":
            return "subir"

        if robot in ("H", "I"):
            return "ir_Izquierda"
        
        if robot == "G":
            return "bajar"
        
        return "nada"
    
class AgenteReactivoModeloNueveCuartosEstocástico(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo, donde el agente no tiene seguro el realizar las acciones 

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ["A",
        "sucio", "sucio", "sucio",
        "sucio", "sucio", "sucio",
        "sucio", "sucio", "sucio"]

        self.acciones=["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    
    def Accion_Movimiento(self, movimiento_deseado):
        """
        Una función general para los movimientos que quiera realizar el agente, considerando sus probabilidades
        
        :param self: el mismo agente
        :param movimiento_deseado: la acción que espera realizar el agente
        """
    
        r=random()

        if (r<0.80):
            return movimiento_deseado
        elif (r<0.90):
            return "nada"
        else: 
            return choice(self.acciones)

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        idx = "ABCDEFGHI".index(robot)
        self.modelo[idx + 1] = situación

        #self.modelo[1:4] - primer piso
        #self.modelo[4:7] - segundo piso
        #self.modelo[7:10] - tercer piso

        #Cuando todos los pisos estan limpios no hace nada
        if all(x == "limpio" for x in self.modelo[1:]):
            return "nada"

        if situación == "sucio":
            if random()< 0.80:
                return "limpiar"
            else: 
                return "nada"

        # si esta todo el primer esta piso limpio ir al segundo
        if robot == "C" and all(x == "limpio" for x in self.modelo[1:4]):
            return self.Accion_Movimiento("subir")

        # si esta todo el segundo esta piso limpio ir al tercer
        if robot == "F" and all(x == "limpio" for x in self.modelo[4:7]):
            return self.Accion_Movimiento("subir")

        # si esta todo el tercer esta piso limpio ir abajo
        #if robot == "G" and all(x == "limpio" for x in self.modelo[7:10]):
        #   return "bajar"
        
        # si esta todo el segundo esta piso limpio ir abajo
        #if robot == "D" and all(x == "limpio" for x in self.modelo[4:7]):
        #    return "bajar"
        
        #el modelo en los cuartos del centro determina cual cuarto ya limpie? para ir al contrario
        if robot == "B":
            return self.Accion_Movimiento("ir_Izquierda") if self.modelo[1] == "sucio" else self.Accion_Movimiento("ir_Derecha")

        if robot == "E":
            return self.Accion_Movimiento("ir_Izquierda") if self.modelo[4] == "sucio" else self.Accion_Movimiento("ir_Derecha")

        if robot == "H":
            return self.Accion_Movimiento("ir_Izquierda") if self.modelo[7] == "sucio" else self.Accion_Movimiento("ir_Derecha")

        #Movimientos basicos
        if robot in ("A", "D", "G"):
            return self.Accion_Movimiento("ir_Derecha")

        if robot in ("C", "F", "I"):
            return self.Accion_Movimiento("ir_Izquierda")
        
        return "nada"


def prueba_agente(agente):
    estado_inicial = (
        "A",
        "sucio", "sucio", "sucio",
        "sucio", "sucio", "sucio",
        "sucio", "sucio", "sucio")

    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            NueveCuartos(),
            agente,
            estado_inicial,
            200
        ),
        estado_inicial
    )

def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]))

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente(AgenteReactivoModeloNuevecuartos())

    #El aleatorio toma demasiado costo y pasos para no terminar de limpiar con seguridad
    #en su contrario el Agente Reactivo con modelo mantiene el costo al minimo posible así como 
    #terminar en menos pasos y quedarse sin hacer nada ahorrando "energia"

    print("Prueba del entorno con un agente reactivo ciego con modelo")
    prueba_agente(AgenteReactivoModeloNueveCuartosCiego())

    #El agente aleatorio sigue siendo demasiado costoso para no asegurar el hecho de tener todo limpio
    #el agente ciego solo sigue una rutina predeterminada no le importaria si cambiaramos el estado de la prueba
    #por limitaciones de movimiento termina siendo más barato que el reactivo con modelo ya que va al tercer piso y regresa
    #al contrario que el reactivo que siempre intenta tener limpio todo un nivel
    #pero aun me parece mejor el agente reactivo con modelo ya que este sería más eficiente en otros entornos 
    #por ejemplo donde ya tengamos algunos cuartos limpios ya que el Agente ciego no podrá saber esto y los limpiaria igualmente

    print("Prueva del entorno con un agente reactivo Estocástico")
    prueba_agente(AgenteReactivoModeloNueveCuartosEstocástico())

    #Es mucho mejor que el agente aleatorio, ya que sus acciones no son totalmente aleatorias
    #si tine una rutina que seguír solo que le cuesta un poco más por sus factores de aleatoridad
    #no he visto nungun caso donde necesite más de los 200 pasos para terminar de limpiar los cuartos
    #no diferencia su costo mucho más que el de los otros Agentes Reactivos 
    

if __name__ == "__main__":
    test()

