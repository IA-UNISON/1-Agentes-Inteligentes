#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'dante_tostado'

import entornos_f
import entornos_o
import random
from random import choice

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos.

    El estado se define como (robot, A, B, C, D, E, F, G, H, I)
    los cuartos del primer nivel son A, B, C
    los cuartos del segundo nivel son D, E, F
    los cuartos del tercer nivel son G, H, I
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F", "G", "H", "I"
    A, B, C, D, E, F, G, H, I pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").
    La acción de "subir" solo es legal en los primeros dos pisos, en los cuartos de la derecha, 
    mientras que la acción de "bajar" solo es legal en los dos pisos de arriba de arriba y en el cuarto de la izquierda.
    Todas las demás acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los nueve cuartos están sucios
        
        """
        self.x = x0[:]
        self.costo = 0

    def accion_legal(self, accion):
        return accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")
        
        robot = self.x[0]
        
        indice = " ABCDEFGHI".find(robot)
        
        # Costos
        costo_accion = 0
        if accion == "limpiar":
            costo_accion = 1  
        elif accion in ("ir_Derecha", "ir_Izquierda"):
            costo_accion = 2
        elif accion in ("subir", "bajar"):
            costo_accion = 3
        self.costo += costo_accion
        
        if accion == "limpiar":
            self.x[indice] = "limpio"
            
        elif accion == "ir_Derecha":
            # Si no esta en borde derecho (C, F, I son índices 3, 6, 9)
            if indice % 3 != 0: 
                # Moverse a la derecha es sumar 1 (A->B, D->E)
                self.x[0] = " ABCDEFGHI"[indice + 1]
                
        elif accion == "ir_Izquierda":
            # Si no esta en borde izquierdo (A, D, G son índices 1, 4, 7)
            if (indice - 1) % 3 != 0: 
                # Moverse a la izquierda es restar 1 (B->A, E->D)
                self.x[0] = " ABCDEFGHI"[indice - 1]
        
        elif accion == "subir":
            # Solo legal en pisos 1 y 2, cuartos derecha (C y F). Osea indices 3 y 6.
            if indice in (3, 6):
                # Subir de C a F es sumar 3.
                self.x[0] = " ABCDEFGHI"[indice + 3]
                
        elif accion == "bajar":
            # Solo legal en pisos 2 y 3, cuarto izquierda (D y G). Osea indices 4 y 7.
            if indice in (4, 7):
                # Bajar de D a A es restar 3.
                self.x[0] = " ABCDEFGHI"[indice - 3]

    def percepcion(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)

class AgenteReactivoNuevecuartos(entornos_o.Agente):
    """
    Un agente reactivo para el entorno de nueve cuartos

    """
    def __init__(self):
        self.modelo = ['A'] + ['sucio'] * 9

    def programa(self, percepcion):
        robot_real, situacion_real = percepcion
        
    # Actualizar modelo interno
        self.modelo[0] = robot_real
        indice_robot = " ABCDEFGHI".find(robot_real)
        self.modelo[indice_robot] = situacion_real    
    
    # Verifica el estado de limpieza de todos los cuartos
        if all(estado == 'limpio' for estado in self.modelo[1:]):
            return 'nada'
    
    # Si esta sucio, limpiar
        if situacion_real == 'sucio':
            return 'limpiar'
    
    # Si está limpio, moverse en forma de ciclo por los cuartos piso por piso siguiendo las escaleras permitidas.
        if robot_real in ['A', 'B']:
            return 'ir_Derecha'
        
        elif robot_real == 'C':
            return 'subir'
        
        elif robot_real == 'F':
            if self.modelo[4] == 'sucio' or self.modelo[5] == 'sucio': 
                 return 'ir_Izquierda'
            return 'subir'
        
        elif robot_real == 'D':
            if self.modelo[5] == 'sucio': 
                return 'ir_Derecha'
            return 'bajar'
        
        elif robot_real == 'E':
            if self.modelo[4] == 'sucio':
                return 'ir_Izquierda'
            return 'ir_Derecha'
        
        elif robot_real in ['I', 'H']:
            return 'ir_Izquierda'
        
        elif robot_real == 'G':
            return 'bajar'  
        
        return 'nada'  # Acción default si no se cumple ninguna condición
    

class AgenteReactivoSimpleNueveCuartos(entornos_o.Agente):
    """
    Agente reactivo simple (sin memoria).
    Patrulla el entorno siguiendo una ruta fija.
    Nunca se detiene porque no sabe si ya terminó.
    """
    def programa(self, percepcion):
        robot, situacion = percepcion

        # Si está sucio, limpiar
        if situacion == 'sucio':
            return 'limpiar'

        # Reglas de movimiento 
        # Piso 1: A -> B -> C
        if robot == 'A': return 'ir_Derecha'
        if robot == 'B': return 'ir_Derecha'
        
        # Subidas (Por la derecha)
        if robot == 'C': return 'subir'   
        if robot == 'F': return 'subir'   

        # Piso 3: I -> H -> G
        if robot == 'I': return 'ir_Izquierda'
        if robot == 'H': return 'ir_Izquierda'
        
        # Bajada (Por la izquierda)
        if robot == 'G': return 'bajar'   # De G baja a D

        # Piso 2: D -> E -> F
        if robot == 'D': return 'ir_Derecha'
        if robot == 'E': return 'ir_Derecha' 
        
        # Si ninguna regla aplica, hacer nada
        return 'nada'

class NueveCuartosCiego(NueveCuartos):
    """
    Entorno ciego: El robot no sabe si el cuarto está sucio o limpio.
    Solo sabe en qué cuarto se encuentra.
    """
    def percepcion(self):
        # Solo regresa la ubicación del robot 
        return self.x[0]
    
class AgenteReactivoModeloNueveCuartosCiego(AgenteReactivoNuevecuartos):
    """
    Agente para entorno ciego. 
    Como no ve la suciedad, asume que todo está sucio al inicio.
    Cuando limpia, actualiza su modelo interno asumiendo que funcionó.
    """
    def __init__(self):
        # Inicializa con todo sucio
        self.modelo = ['A'] + ['sucio'] * 9

    def programa(self, percepcion):
        robot_real = percepcion 
        
        # Actualizar posición en el modelo 
        self.modelo[0] = robot_real
        indice_robot = " ABCDEFGHI".find(robot_real)
        
        # Revisar modelo para ver si cree que está sucio
        situacion_creida = self.modelo[indice_robot]

        # Lógica de decisión
        accion = 'nada'
        
        # Si ya cree que todo está limpio, parar
        if all(estado == 'limpio' for estado in self.modelo[1:]):
            accion = 'nada'
            
        # Si cree que está sucio, limpiar
        elif situacion_creida == 'sucio':
            accion = 'limpiar'
        
        # Si cree que está limpio, moverse
        else:
            if robot_real in ['A', 'B']: accion = 'ir_Derecha'
            elif robot_real == 'C': accion = 'subir'
            elif robot_real == 'F':
                if self.modelo[4] == 'sucio' or self.modelo[5] == 'sucio': accion = 'ir_Izquierda'
                else: accion = 'subir'
            elif robot_real == 'D':
                if self.modelo[5] == 'sucio': accion = 'ir_Derecha'
                else: accion = 'bajar'
            elif robot_real == 'E':
                if self.modelo[4] == 'sucio': accion = 'ir_Izquierda'
                else: accion = 'ir_Derecha'
            elif robot_real in ['I', 'H']: accion = 'ir_Izquierda'
            elif robot_real == 'G': accion = 'bajar'

        # Asume que queda limpio si decidió limpiar
        if accion == 'limpiar':
            self.modelo[indice_robot] = 'limpio'
            
        return accion

class NueveCuartosEstocastico(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos estocástico.

    El estado se define como (robot, A, B, C, D, E, F, G, H, I)
    los cuartos del primer nivel son A, B, C
    los cuartos del segundo nivel son D, E, F
    los cuartos del tercer nivel son G, H, I
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F", "G", "H", "I"
    A, B, C, D, E, F, G, H, I pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").
    La acción de "subir" solo es legal en los primeros dos pisos, en los cuartos de la derecha, 
    mientras que la acción de "bajar" solo es legal en los dos pisos de arriba de arriba y en el cuarto de la izquierda.
    Todas las demás acciones son válidas en todos los estados.

    Cuando el agente decide aspirar, el 80% de las veces limpiara pero el 20% (aleatorio) dejara sucio el cuarto. 
    Igualmente, cuando el agente decide cambiar de cuarto, se cambia correctamente de cuarto el 80% de la veces, el 10% de la veces 
    se queda en su lugar y el 10% de las veces realiza una acción legal aleatoria.

    """
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los nueve cuartos están sucios
        
        """
        self.x = x0[:]
        self.costo = 0

    def accion_legal(self, accion):
        return accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")

    def _acciones_legales_desde(self, robot):
        "Acciones permitidas desde la posición actual del robot"
        acciones = ["limpiar", "nada"]
        indice = " ABCDEFGHI".find(robot)

        # Movimiento horizontal
        if indice % 3 != 0:
            acciones.append("ir_Derecha")
        if (indice - 1) % 3 != 0:
            acciones.append("ir_Izquierda")

        # Movimiento vertical
        if indice in (3, 6):
            acciones.append("subir")
        if indice in (4, 7):
            acciones.append("bajar")

        return acciones

    def _costo_accion(self, accion):
        if accion == "limpiar":
            return 1
        if accion in ("ir_Derecha", "ir_Izquierda"):
            return 2
        if accion in ("subir", "bajar"):
            return 3
        return 0  # nada

    def _mover_deterministico(self, accion, indice):
        "Aplica movimiento sin estocasticidad usando el índice actual."
        if accion == "ir_Derecha" and indice % 3 != 0:
            self.x[0] = " ABCDEFGHI"[indice + 1]
        elif accion == "ir_Izquierda" and (indice - 1) % 3 != 0:
            self.x[0] = " ABCDEFGHI"[indice - 1]
        elif accion == "subir" and indice in (3, 6):
            self.x[0] = " ABCDEFGHI"[indice + 3]
        elif accion == "bajar" and indice in (4, 7):
            self.x[0] = " ABCDEFGHI"[indice - 3]

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot = self.x[0]
        indice = " ABCDEFGHI".find(robot)

        accion_efectiva = accion

        # Limpieza y movimiento estocástico
        if accion == "limpiar":
            # 80% limpia, 20% falla
            if random.random() < 0.8:
                self.x[indice] = "limpio"
            # El costo se agrega después

        elif accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar"):
            tiro = random.random()
            if tiro < 0.8:
                accion_efectiva = accion
            elif tiro < 0.9:
                accion_efectiva = "nada"  # Se queda en el lugar
            else:
                accion_efectiva = choice(self._acciones_legales_desde(robot))

            # Ejecutar la acción 
            if accion_efectiva in ("ir_Derecha", "ir_Izquierda", "subir", "bajar"):
                self._mover_deterministico(accion_efectiva, indice)
            elif accion_efectiva == "limpiar":
                if random.random() < 0.8:
                    self.x[indice] = "limpio"

        elif accion == "nada":
            accion_efectiva = "nada"

        # Costo basado en la acción realizada
        self.costo += self._costo_accion(accion_efectiva)

    def percepcion(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]

class AgenteReactivoModeloEstocastico(AgenteReactivoNuevecuartos):
    pass

def test():
    """
    Prueba del entorno y los agentes
    """
    print("Prueba del entorno de nueve cuartos con Agente Aleatorio")
    entornos_o.simulador(
        NueveCuartos(),
        AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']),
        200
    )

    print("\nPrueba del entorno de nueve cuartos con Agente Reactivo")
    entornos_o.simulador(
        NueveCuartos(),
        AgenteReactivoNuevecuartos(),
        200
    )

    print("\nPrueba con Agente Reactivo Simple de nueve cuartos")
    entornos_o.simulador(
        NueveCuartos(),
        AgenteReactivoSimpleNueveCuartos(),
        200 
    )
    
    print("Prueba con Agente Ciego basado en Modelo de nueve cuartos")
    entornos_o.simulador(
        NueveCuartosCiego(), 
        AgenteReactivoModeloNueveCuartosCiego(), 
        200
    )
    
    print("Prueba del entorno de nueve cuartos estocástico con Agente basado en Modelo" )
    entornos_o.simulador(
        NueveCuartosEstocastico(),
        AgenteReactivoModeloEstocastico(),
        200
    )
 
 # Conclusiones del test:   
    # El agente aleatorio tiene un costo muy alto pq no sigue una estrategia y tarda mucho tiempo en limpiar todos los cuartos.
    # Costo final del aleatorio tras 200 iteraciones: 368  (adjunto output):
    # 199    ['I', 'limpio', 'limpio', 'limpio', 'sucio', 'limpio', 'sucio', 'limpio', 'limpio', 'limpio']       ir_Izquierda               368
    
    # Por otro lado el agente basado en modelo si tiene una estrategia de barrido circular que logra limpiar todos los cuartos con un costo total mas bajo.
    # El basado en modelo no necesito llegar al limite de 200 iteraciones para limpiar todos los cuartos si no que ocupo solo 20 - 21 si contamos la primera que no hizo nada.
    # El costo final del basado en modelo tras 200 iteraciones: 37 (adjunto output):
    # 19    ['H', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'sucio', 'limpio', 'limpio']       ir_Izquierda                34
    # 20    ['G', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'sucio', 'limpio', 'limpio']         limpiar                   36
    # 21    ['G', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio']           nada                    37
    #  22    ['G', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio']           nada                    37
    
    # El agente reactivo simple tiene termino de limpiar en la iteracion 17 (adjunto output):
    # 16    ['E', 'limpio', 'limpio', 'limpio', 'limpio', 'sucio', 'limpio', 'limpio', 'limpio', 'limpio']         limpiar                   27
    # 17    ['E', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio']        ir_Derecha                 28
    # 18    ['F', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio', 'limpio']          subir                    30
    # Pero al no tener memoria sigue patrullando y limpiando innecesariamente, aumentando su costo total.
    # El costo final del basado en modelo tras 200 iteraciones: 453, es decir el mas alto de los 3:

    # Por lo tanto podemos concluir que el agente basado en modelo es mucho mas eficiente que el aleatorio y el reactivo simple en este entorno de nueve cuartos.
    # Esto se debe a que el agente basado en modelo si tiene una estrategia de limpieza y no depende meramente del azar, por lo cual yo lo considero mejor que el aleatorio.
    # Y ademas al tener memoria del estado de los cuartos puede decidir cuando detenerse, a diferencia del reactivo simple que sigue patrullando sin necesidad y se queda indefinidamente.
    
    
    

if __name__ == "__main__":
    test()
    
# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python