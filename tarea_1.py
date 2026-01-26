#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Oliver Ruiz Beltran'

import entornos_o
from random import choice, random


class NueveCuartos(entornos_o.Entorno):
    '''
	Clase para un entorno de nueve cuartos. 

    El estado se define como (robot, A, B, C, D, E, F, G, H, I)
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F", "G", "H", "I"
    A, B, C, D, E, F, G, H y I pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_Derecha", "ir_Izquierda", "subir", "bajar","limpiar", "nada").
    Todas las acciones son válidas en todos los estados excepto en los siguientes estados 
    "subir": solo es legal en los primeros dos pisos en los cuartos de la derecha.
    "bajar": solo es legal en el tercer y segundo piso en el cuarto de la izquierda.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
	'''
 
 
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
            """
            Por default inicialmente el robot está en A y los nueve cuartos
            están sucios

            """
            self.x = x0[:]
            self.costo = 0
    def accion_legal(self, accion):
        if accion == "nada" or accion == "limpiar":
                return True
                
        robot = self.x[0]
        """  
        ['A', 'D', 'G']
        ['B', 'E', 'H']
        ['C', 'F', 'I']
        """
        if accion == "subir":
            return robot in ['C', 'F']
                
        if accion == "bajar":
            return robot in ['G', 'D']
                
        if accion == "ir_Derecha":
            return robot not in ['C', 'F', 'I']
                
        if accion == "ir_Izquierda":
            return robot not in ['A', 'D', 'G']
                
        return False
    def transicion(self, accion):
            
        if not self.acción_legal(accion):
            raise ValueError("La acción no es legal para este estado")
        robot, a, b, c, d, e, f, g, h, i = self.x
        if (accion != "nada" or 
                a == "sucio" or b == "sucio" or c == "sucio" or 
                d == "sucio" or e == "sucio" or f == "sucio" or 
                g == "sucio" or h == "sucio" or i == "sucio"):
                self.costo += 1

        if accion in ["ir_Derecha", "ir_Izquierda"]:
                self.costo += 1
        elif accion in ["subir", "bajar"]:
                self.costo += 2

        if accion == "limpiar":
            
            self.x[" ABCDEFGHI".find(robot)] = "limpio"
                
        elif accion == "ir_Derecha":
            self.x[0] = " ABCDEFGHI"[" ABCDEFGHI".find(robot) + 1]
                
        elif accion == "ir_Izquierda":
            self.x[0] = " ABCDEFGHI"[" ABCDEFGHI".find(robot) - 1]
                
        elif accion == "subir":
            if robot == 'C': self.x[0] = 'F'
            elif robot == 'F': self.x[0] = 'I'
                
        elif accion == "bajar":
            if robot == 'G': self.x[0] = 'D'
            elif robot == 'D': self.x[0] = 'A'
    def percepcion(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]

class AgenteAleatorio(entornos_o.Agente):
    
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        robot = percepcion[0]
        acciones_validas = []
        
        for accion in self.acciones:
            es_valida = False
            if accion == "nada" or accion == "limpiar":
                es_valida = True
            elif accion == "subir" and robot in ['C', 'F']:
                es_valida = True
            elif accion == "bajar" and robot in ['G', 'D']:
                es_valida = True
            elif accion == "ir_Derecha" and robot not in ['C', 'F', 'I']:
                es_valida = True
            elif accion == "ir_Izquierda" and robot not in ['A', 'D', 'G']:
                es_valida = True
            
            if es_valida:
                acciones_validas.append(accion)
                
        return choice(acciones_validas)

class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        self.modelo[0] = robot
        self.modelo[" ABCDEFGHI".find(robot)] = situacion
        

        # Revisamos si hay algún cuarto sucio
        if 'sucio' not in self.modelo[1:]:
            return 'nada'

        # Si estamos sobre suciedad limpiar
        if situacion == 'sucio':
            self.modelo[" ABCDEFGHI".find(robot)] = 'limpio' 
            return 'limpiar'

        # Moverse para a los demas cuartos
        
        if robot == 'A': return 'ir_Derecha'
        if robot == 'B': return 'ir_Derecha'
        if robot == 'C': return 'subir'
        
        if robot == 'F':
            if self.modelo[5] == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'subir' 
        
        if robot == 'E':
            return 'ir_Derecha'

        if robot == 'I': return 'ir_Izquierda'
        if robot == 'H': return 'ir_Izquierda'
        if robot == 'G': return 'bajar'
        if robot == 'D': return 'bajar'
        
        return 'nada' 

class NueveCuartosCiego(NueveCuartos):
    """
    El agente sabe donde esta pero no sabe si los demas cuartos estan sucios
    """
    def percepcion(self):
        return self.x[0]

class AgenteReactivoModeloNueveCuartosCiego(entornos_o.Agente):
    
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot = percepcion
        
        self.modelo[0] = robot

        if 'sucio' not in self.modelo[1:]:
            return 'nada'

        if self.modelo[" ABCDEFGHI".find(robot)] == 'sucio':
            self.modelo[" ABCDEFGHI".find(robot)] = 'limpio' 
            return 'limpiar'


        if robot == 'A': return 'ir_Derecha'
        if robot == 'B': return 'ir_Derecha'
        if robot == 'C': return 'subir'

        if robot == 'F':
            if self.modelo[5] == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'subir'

        if robot == 'E': return 'ir_Derecha'
        if robot == 'I': return 'ir_Izquierda'
        if robot == 'H': return 'ir_Izquierda'
        if robot == 'G': return 'bajar'
        if robot == 'D': return 'bajar'

        return 'nada'

class NueveCuartosEstocastico(NueveCuartos):
    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f, g, h, i = self.x
        
        if (accion != "nada" or
                a == "sucio" or b == "sucio" or c == "sucio" or
                d == "sucio" or e == "sucio" or f == "sucio" or
                g == "sucio" or h == "sucio" or i == "sucio"):
            self.costo += 1

        if accion in ["ir_Derecha", "ir_Izquierda"]:
            self.costo += 1
        elif accion in ["subir", "bajar"]:
            self.costo += 2

        if accion == "limpiar":
            if random() < 0.8:
                self.x[" ABCDEFGHI".find(robot)] = "limpio"
            
        elif accion in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]:
            rand = random()
            
            accion_a_ejecutar = accion 
            
            if rand < 0.8:
                 pass
                
            elif rand < 0.9:
                accion_a_ejecutar = "nada"
                
            else:
                posibles = ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]
                validas = [act for act in posibles if self.accion_legal(act)]
                accion_a_ejecutar = choice(validas)

            if accion_a_ejecutar == "ir_Derecha":
                self.x[0] = " ABCDEFGHI"[" ABCDEFGHI".find(robot) + 1]

            elif accion_a_ejecutar == "ir_Izquierda":
                self.x[0] = " ABCDEFGHI"[" ABCDEFGHI".find(robot) - 1]

            elif accion_a_ejecutar == "subir":
                if robot == 'C': self.x[0] = 'F'
                elif robot == 'F': self.x[0] = 'I'

            elif accion_a_ejecutar == "bajar":
                if robot == 'G': self.x[0] = 'D'
                elif robot == 'D': self.x[0] = 'A'


class AgenteReactivoEstocastico(AgenteReactivoModeloNueveCuartos):
    pass

def test():
    x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    print("\n" + "="*50)
    print("PRUEBA 1: Agente aleatorio")
    print("="*50)
    entornos_o.simulador(NueveCuartos(x0), 
                         AgenteAleatorio(acciones), 
                         200)

    print("\n" + "="*50)
    print("PRUEBA 2: Agente reactivo")
    print("="*50)
    entornos_o.simulador(NueveCuartos(x0), 
                         AgenteReactivoModeloNueveCuartos(), 
                         200)
    print("\n" + "="*50)
    print("PRUEBA 3: Agente aleatorio ciego")
    print("="*50)
    entornos_o.simulador(NueveCuartosCiego(x0),
                         AgenteAleatorio(acciones),
                         200)

    print("\n" + "="*50)
    print("PRUEBA 3.5: Agente reactivo ciego")
    print("="*50)
    entornos_o.simulador(NueveCuartosCiego(x0),
                         AgenteReactivoModeloNueveCuartosCiego(),
                         200)
    print("\n" + "="*50)
    print("PRUEBA 4: Agente aleatorio estocastico")
    print("="*50)
    entornos_o.simulador(NueveCuartosEstocastico(x0),
                         AgenteAleatorio(acciones),
                         200)

    print("\n" + "="*50)
    print("PRUEBA 4.5: Agente reactivo estocastico")
    print("="*50)
    entornos_o.simulador(NueveCuartosEstocastico(x0),
                         AgenteReactivoEstocastico(),
                         200)

if __name__ == "__main__":
    test()
# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

