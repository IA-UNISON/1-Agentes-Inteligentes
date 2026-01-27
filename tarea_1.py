#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Melina González Méndez'

import entornos_f
import entornos_o
from random import choice

#NueveCuartos
class NueveCuartos(entornos_f.Entorno):
     """
     Clase para un entorno de nueve cuartos (3 pisos x 3 cuartos). 
     
                  [G   H   I    Piso 3
     Cuartos =     D   E   F    Piso 2
                   A   B   C]   Piso 1

     El estado se define como (robot, cuartos)
     donde el robot puede estar en cualquier cuarto. Cada cuarto tiene los valores "limpio" o "sucio".

     Acciones: ["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]

    Costos: Cada accion tiene un costo asociado.
             0 si todos los cuartos están limpios y la acción es nada.
             3 si la acción es subir o bajar.
             2 si la accion es ir a la derecha o ir a la izquerda.
             1 si la accion es limpiar
             Si la accion no es legal, el estado no cambia y el costo es 0.
     """
     #Reglas:
     cuartos = ("A","B","C","D","E","F","G","H","I")
     derecha = {"A":"B", "B":"C", "D":"E", "E":"F", "G":"H", "H":"I"}
     izquierda = {"C":"B", "B":"A", "F":"E", "E":"D", "I":"H", "H":"G"}
     subir = {"C":"F", "F":"I"}
     bajar = {"G":"D", "D":"A"}

     def accion_legal(self, estado, accion):
        """
       Revisa si la acción es legal. Para ello debe de cumplir con las siguientes reglas:
        ir_Derecha: A -> B, B -> C, D->E, E->F, G->H, H->I
 	    ir_Izquierda: C-> B, B-> A, F-> E, E->D, I->H, H -> G
        subir: C->F, F->I (solo legal en los primeros dos pisos, en los cuartos de la derecha).
	    bajar: G->D, D->A (solo legal en los dos pisos de arriba, en los cuartos de la izquierda).
        limpiar: Cambia el estado del cuarto actual a limpio.
        nada: La accion no hace ningún cambio en el entorno.

        """
        if isinstance(estado, str):
            robot = estado
        else:
            robot = estado[0]

        if accion == "ir_derecha":
            return robot in self.derecha
        if accion == "ir_izquierda":
            return robot in self.izquierda
        if accion == "subir":
            return robot in self.subir
        if accion == "bajar":
            return robot in self.bajar
        if accion in ("limpiar", "nada"):
            return True
        return False
     
     def transicion(self, estado, accion):
         """
         Aplica la acción al estado. Si la acción no es legal, el estado se queda igual.
         """
         robot, cuartos = estado

         cuartos_nuevo = dict(cuartos)

         #Comprobar si estan limpios todos los cuartos
         todolimpio = True
         for q in self.cuartos:
             if cuartos_nuevo[q] != "limpio":
                 todolimpio = False
                 break
         
         #Costo
         c_local = (0 if (todolimpio and accion == "nada") else
                    3 if accion in ("subir", "bajar") else 
                    2 if accion in ("ir_derecha", "ir_izquierda") else 1)
         
         if not self.accion_legal(estado, accion):
             return (robot, cuartos_nuevo), 0
         if accion == "ir_derecha":
             robot = self.derecha[robot]
         elif accion == "ir_izquierda":
             robot = self.izquierda[robot]
         elif accion == "subir":
             robot = self.subir[robot]
         elif accion == "bajar":
             robot = self.bajar[robot]
         elif accion == "limpiar":
             cuartos_nuevo[robot] = "limpio"
         elif accion == "nada":
             pass
         
         return (robot, cuartos_nuevo), c_local

     def percepcion(self, estado):
         """
         Muestra donde está el robot y si el cuarto actual esta limpio o sucio.
         """
         robot, cuartos = estado
         return (robot, cuartos[robot])

class AgenteAleatorio(entornos_f.Agente):
    """
    Agente que no planea, no recuerda y no intenta optimizar. Solo elige acciones al azar y su comportamiento es impredecible.
    """
    def __init__(self, entorno):
        self.entorno = entorno
        self.acciones = ("ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada")

    def programa(self, percepcion):
        estado = percepcion

        #Filtro las acciones: Se conservan las que son legales en el estado actual.
        legales = [a for a in self.acciones if self.entorno.accion_legal(estado, a)]
        return choice(legales)

class AgenteReactivoModelo(entornos_f.Agente):
     """
     Agente que tiene memoria, recuerda que cuartos limpió y toma decisiones inteligentes.
     Primero se inicializa en el peor de los casos (todos los cuartos sucios) y se guarda la posición actual del robot.
     """
     def __init__(self):
        self.modelo = {q: "sucio" for q in ("A","B","C","D","E","F","G","H","I")}
        self.robot = "A"

     def programa(self, percepcion):
        robot, situacion = percepcion
        self.robot = robot
        self.modelo[robot] = situacion

        #Si el cuarto esta sucio, entonces limpio
        if situacion == "sucio":
            self.modelo[robot] = "limpio"
            return "limpiar"

        #Todos los cuartos estan limpios, entonces no hago nada
        if all(self.modelo[q] == "limpio" for q in self.modelo):
            return "nada"
        
        #Explorar cuartos vecinos (ir_derecha, ir_izquerda, subir, bajar)
        if robot in NueveCuartos.derecha:
            sig = NueveCuartos.derecha[robot]
            if self.modelo[sig] == "sucio":
                return "ir_derecha"
        
        if robot in NueveCuartos.izquierda:
            sig = NueveCuartos.izquierda[robot]
            if self.modelo[sig] == "sucio":
                return "ir_izquierda"
            
        if robot in NueveCuartos.subir:
            sig = NueveCuartos.subir[robot]
            if self.modelo[sig] == "sucio":
                return "subir"
            
        if robot in NueveCuartos.bajar:
            sig = NueveCuartos.bajar[robot]
            if self.modelo[sig] == "sucio":
                return "bajar"
            
        #Para evitar que el agente se quede estancado. Explorar el entorno:
        if robot in NueveCuartos.derecha:
            return "ir_derecha"
        if robot in NueveCuartos.izquierda:
            return "ir_izquierda"
        if robot in NueveCuartos.subir:
            return "subir"
        if robot in NueveCuartos.bajar:
            return "bajar"
        return "nada"

class NueveCuartosCiego(NueveCuartos):
    """
    Este agente solo sabe la ubicacion en la que está, pero no sabe si el cuarto está limpio o sucio.
    """
    def percepcion(self, estado):
        robot, _ = estado
        return robot
    
class AgenteReactivoNueveCuartosCiego(AgenteReactivoModelo):
    """
    Este agente no puede ver si un cuarto esta sucio o limpio, por lo que recorre todos los cuartos y los limpia.
    """
    def __init__(self):
        self.cuartos = ("A","B","C","D","E","F","G","H","I")
        self.modelo =  ["?", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    
    def programa(self, percepcion):
        robot = percepcion
        self.modelo[0] = robot

        idx = self.cuartos.index(robot) + 1

        if all(self.modelo[i] == "limpio" for i in range(1,10)):
            return "nada"
        
        if self.modelo[idx] == "sucio":
            self.modelo[idx] = "limpio"
            return "limpiar"
        
        if robot in ("A", "B", "D", "E", "G", "H"):
            return "ir_derecha"
        if robot in ("C", "F"):
            return "subir"
        if robot in ("I"):
            return "ir_izquierda"
        if robot in ("G", "D"):
            return "bajar"

        return "nada"

class AgenteAleatorioNueveCuartos(entornos_f.Agente):
    """
    Un agente que solo regresa una acción al azar entre las acciones legales
    """
    def __init__(self):
        self.acciones = ["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]

    def programa(self, percepcion):
        return choice(self.acciones)

            
def prueba_aleatorio_ciego():
    env = NueveCuartosCiego()
    estado_inicial = ("A", {q: "sucio" for q in env.cuartos})

    agente = AgenteAleatorio(env)
    historial = entornos_f.simulador(env, agente, estado_inicial, T=200)

    print("\n>>> Agente aleatorio (ciego) <<<")
    imprimir_tabla(historial, estado_inicial)

def prueba_agente_modelo():
    env = NueveCuartos()
    estado_inicial = ("A", {q: "sucio" for q in env.cuartos})

    agente = AgenteReactivoModelo()
    historial = entornos_f.simulador(env, agente, estado_inicial, T=200)

    imprimir_tabla(historial, estado_inicial)

def prueba_modelo_ciego():
    env = NueveCuartosCiego()
    estado_inicial = ("A", {q: "sucio" for q in env.cuartos})

    agente = AgenteReactivoNueveCuartosCiego()
    historial = entornos_f.simulador(env, agente, estado_inicial, T=200)
	
    imprimir_tabla(historial, estado_inicial)
            
def prueba_agente_aleatorio():
    env = NueveCuartos()
    estado_inicial = ("A", {q: "sucio" for q in env.cuartos})

    agente = AgenteAleatorio(env)
    historial = entornos_f.simulador(env, agente, estado_inicial, T=200)

    imprimir_tabla(historial, estado_inicial)

def prueba_agente_modelo():
    env = NueveCuartos()
    estado_inicial = ("A", {q: "sucio" for q in env.cuartos})

    agente = AgenteReactivoModelo()
    historial = entornos_f.simulador(env, agente, estado_inicial, T=200)

    imprimir_tabla(historial, estado_inicial)
    
def imprimir_tabla(historial, estado_inicial):
    print("\nSimulación iniciando en:", estado_inicial)
    print()
    print(f"{'Paso':>4} | {'Acción':^12} | {'Robot':^5} | {'Estado cuarto':^14} | {'Costo':>5}")
    print("-" * 55)

    for i, (accion, estado, costo) in enumerate(historial):
        robot, cuartos = estado
        estado_actual = cuartos[robot]

        print(f"{i:>4} | {accion:^12} | {robot:^5} | {estado_actual:^14} | {costo:>5}")

def test():
    print("\n>>> Agente aleatorio <<<")
    prueba_agente_aleatorio()

    print("\n>>> Agente reactivo modelo <<<")
    prueba_agente_modelo()

	print("\n>>> Agente aleatorio (ciego) <<<")
    prueba_aleatorio_ciego()

    print("\n>>> Agente reactivo modelo (ciego) <<<")
    prueba_modelo_ciego()

if __name__ == "__main__":
    test()

"""
Observaciones:
El agente aleatorio realiza muchas acciones innecesarias, como limpiar cuartos ya limpios o ejecutar la acción “nada”, lo que provoca un mayor número de pasos y un costo más alto, ya que no cuenta con memoria ni estrategia.
En cambio, el agente reactivo basado en modelo utiliza memoria para recordar los cuartos visitados y su estado, lo que le permite tomar mejores decisiones y completar la tarea con menor costo y en menos tiempo.
Cuando el agente es ciego , resulta necesario una estrategia de recorrido, pues al no poder distinguir si un cuarto está sucio o limpio, puede quedar atrapado repitiendo acciones sin avanzar de manera efectiva.

"""


