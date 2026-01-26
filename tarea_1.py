#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Juan Pablo Zurita Murillo'

import entornos_o
from random import choice
import random
import copy

## ENTORNOS ##

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos.

    El estado se define como (robot, s0, s1, s2, s3, s4, s5, s6, s7, s8)
    donde robot es una coordenada piso, cuarto.
    Piso y cuarto van de [0, 2]
    Hay tres pisos, tres cuartos en cada uno:
    s0-s2 - piso 0, 
    s3-s5 - piso 1, 
    s6-s8 - piso 2.
    Todos pueden estar sucios o limpios.

    Las acciones válidas en el entorno son ("ir_Derecha", "ir_Izquierda", "subir", "bajar" "limpiar", "nada").
    Solo se puede subir si el robot está en los primeros dos pisos, en los cuartos derechos.
    Solo se puede bajar del segundo piso para arriba, en los cuartos izquierdos.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=None):
        """
        Por default inicialmente el robot está en piso 0, cuarto 0, y todos los cuartos
        están sucios

        """
        if x0 is None:
            x0 = [[0,0]] + ["sucio"] * 9          

        self.x = copy.deepcopy(x0) 
        self.costo = 0

    def accion_legal(self, accion):
        """
        Indica si una acción es legal dentro de la grid 3x3

        """
        piso, cuarto = self.x[0] # La parte que contiene las coordenadas

        if accion == "ir_Derecha":
            return cuarto < 2
        
        elif accion == "ir_Izquierda":
            return cuarto > 0
        
        elif accion == "subir":
            return piso < 2 and cuarto == 2
        
        elif accion == "bajar":
            return piso > 0 and cuarto == 0
        
        elif accion in ("limpiar", "nada"):
            return True
        return False
    
    def transicion(self, accion):
        """
        Lógica de transición entre estados

        """
        if not self.accion_legal(accion):
           return
        
        # Arregla bug visual de posición en simulación
        self.x[0] = self.x[0][:]
        
        piso, cuarto = self.x[0]

        if accion == "limpiar":
            self.costo += 1
            self.x[1 + (3 * piso) + cuarto] = "limpio"

        elif accion == "ir_Derecha":
            self.costo += 2
            self.x[0][1] += 1

        elif accion == "ir_Izquierda":
            self.costo += 2
            self.x[0][1] -= 1

        elif accion == "subir":
            self.costo += 3
            self.x[0][0] += 1

        elif accion == "bajar":
            self.costo += 3
            self.x[0][0] -= 1

    def percepcion(self):
        """
        Indica donde está el robot y el estado (sucio o limpio) del cuarto
        en el que se encuentra

        """
        piso, cuarto = self.x[0]
        return self.x[0], self.x[1 + (3 * piso) + cuarto]

class NueveCuartosCiego(NueveCuartos):
    def percepcion(self):
        return self.x[0] # Regresamos solo donde está el robot

class NueveCuartosEstocastico(NueveCuartos):
   def transicion(self, accion):
        """
        Al aspirar:
        Limpia el 80% de las veces, el 20% deja sucio el cuarto.
        
        Al cambiar de cuarto (incluyendo subir, bajar):
        - Cambia correctamente de cuarto el 80% de la veces
        - Se queda en su lugar el 10% de la veces
        - Acción legal aleatoria el 10% de las veces 

        """
        if not self.accion_legal(accion):
           return
        
        # Arregla bug visual de posición en simulación
        self.x[0] = self.x[0][:]
        
        accion_roll = accion

        if accion in ['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar']:
            roll = random.random()

            if roll > 0.9:
                acciones = ['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar']
                acciones_legales = []

                for accion in acciones:
                    if self.accion_legal(accion):
                        acciones_legales.append(accion)

                accion_roll = choice(acciones_legales)
                    
            elif roll > 0.8:
                accion_roll = 'nada'
            else:
                pass

        piso, cuarto = self.x[0]

        if accion_roll == 'limpiar':
            roll = random.random()

            self.costo += 1

            if roll > 0.8:
                pass # No se limpia
            else:
                self.x[1 + (3 * piso) + cuarto] = "limpio"

        elif accion_roll == "ir_Derecha":
            self.costo += 2
            self.x[0][1] += 1

        elif accion_roll == "ir_Izquierda":
            self.costo += 2
            self.x[0][1] -= 1

        elif accion_roll == "subir":
            self.costo += 3
            self.x[0][0] += 1

        elif accion_roll == "bajar":
            self.costo += 3
            self.x[0][0] -= 1

## AGENTES ##

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)
    
class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = [[0,0]] + ["sucio"] * 9

    def programa(self, percepcion):
        robot, situacion = percepcion
        piso, cuarto = robot

        # Actualiza el modelo interno
        self.modelo[0] = robot

        self.modelo[1 + (3 * piso) + cuarto] = situacion

        if situacion == 'sucio':
            return 'limpiar'
        
        # Si alguno de los pisos debajo está sucio, bajar para limpiar
        piso_0_sucio = 'sucio' in self.modelo[1:4]
        piso_1_sucio = 'sucio' in self.modelo[4:7]

        if piso == 2 and (piso_0_sucio or piso_1_sucio):
            if cuarto > 0:
                return 'ir_Izquierda'
            else:
                return 'bajar'
        
        if piso == 1 and piso_0_sucio:
            if cuarto > 0:
                return 'ir_Izquierda'
            else:
                return 'bajar'
       
        if piso == 0:
            if cuarto < 2:
                return 'ir_Derecha'
            elif cuarto == 2:
                return 'subir'
        
        elif piso == 1:
            cuarto_izq_limpio = (self.modelo[4] == 'limpio')
            
            if not cuarto_izq_limpio and cuarto > 0:
                return 'ir_Izquierda'
           
            elif cuarto < 2:
                return 'ir_Derecha'
            
            elif cuarto == 2:
                return 'subir'
        
        elif piso == 2:
            if cuarto > 0:
                return 'ir_Izquierda'
            else:
                return 'nada'
        
        return 'nada'
    
class AgenteReactivoModeloNueveCuartosCiego(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo, pero el robot no sabe
    la situación del cuarto, solo su propia posición

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = [[0,0]] + ["sucio"] * 9

    def programa(self, percepcion):
        robot = percepcion
        piso, cuarto = robot

        self.modelo[0] = robot

        if self.modelo[1 + (3 * piso) + cuarto] == 'sucio':
            self.modelo[1 + (3 * piso) + cuarto] = 'limpio'
            return 'limpiar'
        
        # Si alguno de los pisos debajo está sucio, bajar para limpiar
        piso_0_sucio = 'sucio' in self.modelo[1:4]
        piso_1_sucio = 'sucio' in self.modelo[4:7]

        if piso == 2 and (piso_0_sucio or piso_1_sucio):
            if cuarto > 0:
                return 'ir_Izquierda'
            else:
                return 'bajar'
        
        if piso == 1 and piso_0_sucio:
            if cuarto > 0:
                return 'ir_Izquierda'
            else:
                return 'bajar'

        if piso == 0:
            if cuarto < 2:
                return 'ir_Derecha'
            elif cuarto == 2:
                return 'subir'
       
        if piso == 0:
            if cuarto < 2:
                return 'ir_Derecha'
            elif cuarto == 2:
                return 'subir'
        
        elif piso == 1:
            cuarto_izq_limpio = (self.modelo[4] == 'limpio')
            
            if not cuarto_izq_limpio and cuarto > 0:
                return 'ir_Izquierda'
            
            elif cuarto < 2:
                return 'ir_Derecha'
            
            elif cuarto == 2:
                return 'subir'
        
        elif piso == 2:
            if cuarto > 0:
                return 'ir_Izquierda'
            else:
                return 'nada'
        
        return 'nada'

class AgenteReactivoModeloNueveCuartosEstocastico(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo para uso
    con el entorno estocástico.

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = [[0,0]] + ["sucio"] * 9
    
    def programa(self, percepcion):
        robot, situacion = percepcion
        piso, cuarto = robot

        # Actualiza el modelo interno
        self.modelo[0] = robot

        self.modelo[1 + (3 * piso) + cuarto] = situacion

        if situacion == 'sucio':
            return 'limpiar'
        
        # Si alguno de los pisos debajo está sucio, bajar para limpiar
        piso_0_sucio = 'sucio' in self.modelo[1:4]
        piso_1_sucio = 'sucio' in self.modelo[4:7]

        if piso == 2 and (piso_0_sucio or piso_1_sucio):
            if cuarto > 0:
                return 'ir_Izquierda'
            else:
                return 'bajar'
        
        if piso == 1 and piso_0_sucio:
            if cuarto > 0:
                return 'ir_Izquierda'
            else:
                return 'bajar'

        if piso == 0:
            if cuarto < 2:
                return 'ir_Derecha'
            elif cuarto == 2:
                return 'subir'
        
        elif piso == 1:
            cuarto_izq_limpio = (self.modelo[4] == 'limpio')
            
            if not cuarto_izq_limpio and cuarto > 0:
                return 'ir_Izquierda'
            
            elif cuarto < 2:
                return 'ir_Derecha'
            
            elif cuarto == 2:
                return 'subir'
        
        elif piso == 2:
            if cuarto > 0:
                return 'ir_Izquierda'
            else:
                return 'nada'
        
        return 'nada'

## TEST ##

def test():
    """
    Prueba del entorno y los agentes

    """
    x0= [[0,0]] + ["sucio"] * 9
    
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']),
                         200)
      
    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(x0), 
                         AgenteReactivoModeloNueveCuartos(), 
                         200)
    
    # En comparación al agente aleatorio, que usualmente ni termina de limpiar todos los cuartos, el agente reactivo
    # con modelo lo hace con solo 31 de costo. Esto por que recorre el edificio de manera eficiente, en forma de símbolo
    # matemático de "existe" o "E volteada".

    # Prueba de vista
    entorno_reluciente = [[0,0]] + ["limpio"] * 9
    
    print("Prueba del entorno ciego con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosCiego(entorno_reluciente), 
                         AgenteReactivoModeloNueveCuartosCiego(), 
                         200)
    
    # El agente ractivo ciego basado en modelo se comporta igual al no ciego si los estados iniciales
    # del entorno son los mismos (todo sucio). Si todo está limpio (como en el test), igual ejecuta la rutina
    # por lo que puede ser más costoso solo por acciones no necesarias. Entonces si lo comparamos al aleatorio,
    # este igual es mucho menos eficiente.
    
    print("Prueba del entorno estocástico con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosEstocastico(x0), 
                         AgenteReactivoModeloNueveCuartosEstocastico(), 
                         200)
    
    # El agente ractivo estocástico basado en modelo varía en costo dentro del rango de 31 a 50 a partir de pruebas.
    # Esto lo hace en promedio 2+ veces más eficiente que el aleatorio.

if __name__ == "__main__":
    test()

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python