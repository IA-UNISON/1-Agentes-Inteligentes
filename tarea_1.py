
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Michell Altamirano Ocejo'

import entornos_o
from random import choice, random
from copy import deepcopy

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos.

    El estado se define como (robot, [["sucio", ...], ["sucio", ...]...])
    donde robot puede tener los valores (0,0), ..., (2, 2)
    y pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"].
    Solo algunas acciones son posibles en algunos estados, por ejemplo, no se puede subir si el robot está en (2,2).
    Solamente se sube por la derecha y se baja por la izquierda.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza.

    """
    
    def __init__(self, x0 = [(0,0), [["sucio" for _ in range(3)] for _ in range(3)]]):
        super().__init__(x0)
        
    def accion_legal(self, accion):
        piso, cuarto = self.x[0]
        if accion == "ir_Derecha":
            return cuarto != 2
        elif accion == "ir_Izquierda":
            return cuarto != 0
        elif accion == "bajar":
            return piso != 0 and cuarto == 0 # Solo bajar por la izquierda
        elif accion == "subir":
            return piso != 2 and cuarto == 2 # Solo subir por la derecha
        else:
            return accion in ["limpiar", "nada"]
    
    def transicion(self, accion):
        if not self.accion_legal(accion):
            accion = "nada"
        
        robot, cuartos = self.x[0], self.x[1]
        cuartos = deepcopy(cuartos) 

        if accion == "limpiar":
            self.costo += 1
            cuartos[robot[0]][robot[1]] = "limpio"
        elif accion == "ir_Derecha":
            self.costo += 2
            robot = (robot[0], robot[1] + 1)
        elif accion == "ir_Izquierda":
            self.costo += 2
            robot = (robot[0], robot[1] - 1)
        elif accion == "bajar":
            self.costo += 3
            robot = (robot[0] - 1, robot[1])
        elif accion == "subir":
            self.costo += 3
            robot = (robot[0] + 1, robot[1])
        elif accion == "nada":
            # Solo cobra si hay suciedad en algunlado
            if "sucio" in [room for floor in cuartos for room in floor]:
                self.costo += 1
            
        self.x = (robot, cuartos)
            
    def percepcion(self):
        robot = self.x[0]
        return robot, self.x[1][robot[0]][robot[1]]
    

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales.

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)
    
class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = [(0,0), [["sucio" for _ in range(3)] for _ in range(3)]]

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot 
        self.modelo[1][robot[0]][robot[1]] = situacion 

        # Decide sobre el modelo interno
        cuartos = self.modelo[1]
        
        if situacion == "sucio":
            return "limpiar"
        
        # Buscar el cuarto sucio ms cercano
        for piso in range(3):
            for cuarto in range(3):
                if cuartos[piso][cuarto] == "sucio":
                    # Si está en el mismo piso
                    if robot[0] == piso:
                        if robot[1] < cuarto:
                            return "ir_Derecha"
                        elif robot[1] > cuarto:
                            return "ir_Izquierda"
                    
                    # Si está en otro piso
                    if robot[0] < piso:
                        # Primero ir a la derecha para subir
                        if robot[1] < 2:
                            return "ir_Derecha"
                        else:
                            return "subir"
                    elif robot[0] > piso:
                        # Primero ir a la izquierda para bajar
                        if robot[1] > 0:
                            return "ir_Izquierda"
                        else:
                            return "bajar"

        return "nada"
    
class NueveCuartosCiego(NueveCuartos):
    """
    Igual que NueveCuartos, pero solo se puede percibir la ubicación del robot, no el estado de limpieza
    """
    
    def percepcion(self):
        return self.x[0]

class AgenteReactivoModeloNueveCuartosCiego(AgenteReactivoModeloNueveCuartos):
    """
    Un agente reactivo basado en modelo, para entornos ciegos

    """

    def programa(self, percepcion):
        robot = percepcion

        # Actualiza la posición en el modelo interno
        self.modelo[0] = robot 

        # Decide sobre el modelo interno
        cuartos = self.modelo[1]
        
        # Si el modelo dice que está sucio aquí, limpiar
        if cuartos[robot[0]][robot[1]] == "sucio":
            print(f"Actualizamos modelo interno: {robot} = 'limpio'")
            cuartos[robot[0]][robot[1]] = "limpio"
            return "limpiar"
        
        # Buscar el cuarto sucio más cercano
        for piso in range(3):
            for cuarto in range(3):
                if cuartos[piso][cuarto] == "sucio":
                    # Si está en el mismo piso
                    if robot[0] == piso:
                        if robot[1] < cuarto:
                            return "ir_Derecha"
                        elif robot[1] > cuarto:
                            return "ir_Izquierda"
                    
                    # Si está en otro piso
                    if robot[0] < piso:
                        # Primero ir a la derecha para subir
                        if robot[1] < 2:
                            return "ir_Derecha"
                        else:
                            return "subir"
                    elif robot[0] > piso:
                        # Primero ir a la izquierda para bajar
                        if robot[1] > 0:
                            return "ir_Izquierda"
                        else:
                            return "bajar"

        return "nada"


class NueveCuartosEstocastico(NueveCuartos):
    """
    Igual que NueveCuartos, pero con limpieza y movimiento estocástico:
        - 80% de probabilidad de limpiar correctamente
        - 80% de probabilidad de moverse correctamente
        - 10% de probabilidad de no hacer nada
        - 10% de probabilidad de moverse aleatoriamente
    
    """
    
    def transicion(self, accion):
        """Realiza la transición de estado según la acción estocástica."""
        if not self.accion_legal(accion):
            accion = "nada"

        robot, cuartos = self.x[0], deepcopy(self.x[1])
        rand_num = random()

        if accion == "limpiar":
            self.costo += 1
            # Limpieza estocástica (80% éxito)
            if rand_num < 0.8:
                cuartos[robot[0]][robot[1]] = "limpio"

        elif accion in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]:
            # Movimiento estocástico
            if rand_num < 0.8:
                robot = self._mover(robot, accion)
            elif rand_num < 0.9:  # 10% no hace nada
                pass
            else:  # 10% acción legal aleatoria
                acciones_posibles = [a for a in ["ir_Izquierda", "ir_Derecha", "subir", "bajar"] 
                                   if self.accion_legal(a)]
                if acciones_posibles:
                    random_accion = choice(acciones_posibles)
                    robot = self._mover(robot, random_accion)
            
            # Costos según acción intentada
            self.costo += 2 if accion in ["ir_Izquierda", "ir_Derecha"] else 3

        elif accion == "nada":
            if "sucio" in [room for floor in cuartos for room in floor]:
                self.costo += 1

        self.x = (robot, cuartos)
        
    def _mover(self, robot, accion):
        """Calcula la nueva posición del robot según la acción."""
        if accion == "ir_Derecha":
            return (robot[0], robot[1] + 1)
        elif accion == "ir_Izquierda":
            return (robot[0], robot[1] - 1)
        elif accion == "subir":
            return (robot[0] + 1, robot[1])
        elif accion == "bajar":
            return (robot[0] - 1, robot[1])
        return robot


def test():
    """
    Prueba de entorno y los agentes
    """
    
    x0 = [(0,0), [["sucio" for _ in range(3)] for _ in range(3)]] # Estado inicial
    acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    
    print("=" * 60)
    print("Prueba 1: Agente Aleatorio en NueveCuartos")
    print("=" * 60)
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteAleatorio(acciones),
                         100)
    
    print("\n" + "=" * 60)
    print("Prueba 2: Agente Reactivo Modelo en NueveCuartos")
    print("=" * 60)
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteReactivoModeloNueveCuartos(),
                         100)
    
    print("\n" + "=" * 60)
    print("Prueba 3: Agente Aleatorio en NueveCuartosCiego")
    print("=" * 60)
    entornos_o.simulador(NueveCuartosCiego(x0),
                         AgenteAleatorio(acciones),
                         100)
    
    print("\n" + "=" * 60)
    print("Prueba 4: Agente Reactivo Modelo Ciego en NueveCuartosCiego")
    print("=" * 60)
    entornos_o.simulador(NueveCuartosCiego(x0),
                         AgenteReactivoModeloNueveCuartosCiego(),
                         200)
    
    print("\n" + "=" * 60)
    print("Prueba 5: Agente Aleatorio en NueveCuartosEstocastico")
    print("=" * 60)
    entornos_o.simulador(NueveCuartosEstocastico(x0),
                         AgenteAleatorio(acciones),
                         100)
    
    print("\n" + "=" * 60)
    print("Prueba 6: Agente Reactivo Modelo en NueveCuartosEstocastico")
    print("=" * 60)
    entornos_o.simulador(NueveCuartosEstocastico(x0),
                         AgenteReactivoModeloNueveCuartos(),
                         200)
    
if __name__ == "__main__":
    test()