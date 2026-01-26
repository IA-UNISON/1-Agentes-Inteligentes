#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'David Casanova'

# Solamente quiero comentar de que este trabajo esta hecho con la ayufs de IA (lo cual es ironico)
# ya que no le entiendo del todo por mi mismo, aun viendo el ejemplo de DosCuartos.
# Procure de hacer el esfuerzo para tratar de enteder el codigo en sí. Deje comentarios
# en los procesos.
# Aunque no me saque buena calificación (lo cual es comprensible) me gustaría discutir
# con usted el programa a fondo para que le pueda entender mejor al menos. Gracias.

import entornos_f
import doscuartos_f
import random

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_f.Entorno):
    """
    Estado: (robot, r0, r1, r2, r3, r4, r5, r6, r7, r8)
    Indices: Piso 1 (0-2), Piso 2 (3-5), Piso 3 (6-8)
    """

    # Aquí definimos las reglas del "juego"

    # Estas son las acciones que podemos llevar a cabo en casillas específicas (David)
    def accion_legal(self, estado, accion):
        robot = estado[0]
        if accion == "subir": return robot in (2, 5)
        if accion == "bajar": return robot in (3, 6)
        if accion == "ir_Derecha": return robot not in (2, 5, 8)
        if accion == "ir_Izquierda": return robot not in (0, 3, 6)
        return accion in ("limpiar", "nada")

    # Aquí definimos un cambio de estado y los costos que conllevan ciertas acciones que causan el cambio de estado (David)
    def transicion(self, estado, accion):
        robot = estado[0]
        habitaciones = list(estado[1:])
        
        if accion == "nada":
            # Costo 0 solo si todo está limpio
            return estado, 0 if all(h == 'limpio' for h in habitaciones) else 1
        
        if accion == "limpiar":
            habitaciones[robot] = "limpio"
            return tuple([robot] + habitaciones), 1
        
        # Movimientos (Horizontal costo 2, Vertical costo 5)
        nuevo_robot = robot
        if accion == "ir_Derecha": nuevo_robot += 1
        elif accion == "ir_Izquierda": nuevo_robot -= 1
        elif accion == "subir": nuevo_robot += 3
        elif accion == "bajar": nuevo_robot -= 3
        
        costo = 5 if accion in ("subir", "bajar") else 2
        return tuple([nuevo_robot] + habitaciones), costo

    # Aquí regresamos el estado en el que nos encontramos y al que vamos a saltar. (David)
    def percepcion(self, estado):
        return estado[0], estado[estado[0] + 1]

class NueveCuartosCiego(NueveCuartos):
    """Agente solo percibe su ubicación."""
    # Para ahorrarnos tiempo, heredamos el codigo de nuestro entorno original, solamente cambiando la manera en la que nuestro objeto "percibe" (David)
    # Aquí simplemente le devolvemos al objeto el cuarto en el que está. Basicamente está a oscuras. Sabe donde está y nada más (David)
    def percepcion(self, estado):
        return estado[0]

class NueveCuartosEstocastico(NueveCuartos):
    """Acciones con 80% de éxito, 10% falla, 10% acción aleatoria."""
    def transicion(self, estado, accion):
        if accion == "nada": return super().transicion(estado, accion)
        
        # Aquí lo dejamos a chance de que una acción tenga efecto o no. (David)
        prob = random.random()
        if accion == "limpiar":
            return super().transicion(estado, accion) if prob < 0.8 else (estado, 1)

            # Igual aquí. (David)
        if accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar"):
            if prob < 0.8:
                return super().transicion(estado, accion)
            elif prob < 0.9:
                return estado, 1
            else:
                acciones = [a for a in ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"] if self.accion_legal(estado, a)]
                return super().transicion(estado, random.choice(acciones))
        return super().transicion(estado, accion)

# Agentes

class AgenteAleatorio(entornos_f.Agente):
    """Simplemente para comparar desempeño."""
    def __init__(self, acciones):
        self.acciones = acciones
        
    def programa(self, _):
        return random.choice(self.acciones)

class AgenteModeloNueveCuartos(entornos_f.Agente):
    """Agente inteligente con memoria para Entorno Normal y Estocástico."""
    def __init__(self):
        self.modelo = [0] + ["sucio"] * 9
    
    def programa(self, percepcion):
        robot, situacion = percepcion
        self.modelo[0], self.modelo[robot+1] = robot, situacion
        
        if all(s == 'limpio' for s in self.modelo[1:]): return 'nada'
        if situacion == 'sucio': return 'limpiar'
        
        if robot < 2: return 'ir_Derecha'
        if robot == 2: return 'subir'
        if robot == 5:
            # Si el piso 2 no está terminado, ir a la izquierda
            if self.modelo[4] == 'sucio' or self.modelo[3+1] == 'sucio':
                return 'ir_Izquierda'
            return 'subir'
        if robot == 4:
            return 'ir_Izquierda' if self.modelo[3+1] == 'sucio' else 'ir_Derecha'
        if robot == 3: return 'ir_Derecha'
        if robot > 6: return 'ir_Izquierda'
        return 'nada'

class AgenteRacionalCiego(entornos_f.Agente):
    """Limpia todo a su paso porque no puede ver."""
    def __init__(self):
        self.limpios = [False] * 9

    def programa(self, robot):
        if not self.limpios[robot]:
            self.limpios[robot] = True
            return 'limpiar'
        if all(self.limpios): return 'nada'
        if robot < 2: return 'ir_Derecha'
        if robot == 2: return 'subir'
        if robot == 5:
            return 'ir_Izquierda' if not (self.limpios[3] and self.limpios[4]) else 'subir'
        if robot == 4:
            return 'ir_Izquierda' if not self.limpios[3] else 'ir_Derecha'
        if robot == 3: return 'ir_Derecha'
        return 'ir_Izquierda' if robot > 6 else 'nada'


# Pruebas

def comparar_agentes():
    estado_inicial = tuple([0] + ["sucio"] * 9)
    acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    print("-" * 30)
    print("1. ENTORNO NORMAL: Modelo vs Aleatorio")
    entornos_f.imprime_simulacion(entornos_f.simulador(NueveCuartos(), AgenteModeloNueveCuartos(), estado_inicial, 200), estado_inicial)
    
    print("-" * 30)
    print("2. ENTORNO CIEGO: Racional Ciego vs Aleatorio")
    entornos_f.imprime_simulacion(entornos_f.simulador(NueveCuartosCiego(), AgenteRacionalCiego(), estado_inicial, 200), estado_inicial)

    print("-" * 30)
    print("3. ENTORNO ESTOCÁSTICO: Modelo vs Aleatorio")
    entornos_f.imprime_simulacion(entornos_f.simulador(NueveCuartosEstocastico(), AgenteModeloNueveCuartos(), estado_inicial, 200), estado_inicial)

if __name__ == "__main__":
    comparar_agentes()