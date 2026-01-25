#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
------------
tarea_1.py
------------
"""
__author__ = 'franciscoricardohernandezastorga'

import entornos_o
from random import choice


class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos distribuidos en 3 pisos.

    El estado se define como (robot, estado_0, estado_1, ..., estado_8)
    donde robot es un entero del 0 al 8 indicando la ubicacion.
    Los estados pueden ser "limpio" o "sucio".

    Distribucion de los cuartos:
    Piso 3: | 6 | 7 | 8 |
    Piso 2: | 3 | 4 | 5 |
    Piso 1: | 0 | 1 | 2 |
    """

    def __init__(self, x0=[0, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en 0 y todos los cuartos
        están sucios

        """
        self.x = x0[:]
        self.costo = 0

    def accion_legal(self, accion):
        """
        Revisa si la acción es válida.
        """
        robot = self.x[0]

        if accion == "subir":
            # Solo se puede subir desde los cuartos 2 y 5
            return robot == 2 or robot == 5

        if accion == "bajar":
            # Solo se puede bajar desde los cuartos 6 y 3
            return robot == 6 or robot == 3

        if accion == "ir_Derecha":
            # No puedes ir a la derecha si ya estás en el borde derecho
            return robot not in [2, 5, 8]

        if accion == "ir_Izquierda":
            # No puedes ir a la izquierda si ya estás en el borde izquierdo
            return robot not in [0, 3, 6]

            # "limpiar" y "nada" siempre son legales
        return True

    def transicion(self, accion):
        if not self.acción_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot = self.x[0]
        if accion == "limpiar":
            self.costo += 1
            self.x[robot + 1] = "limpio"

        elif accion == "ir_Derecha":
            self.costo += 2
            self.x[0] += 1

        elif accion == "ir_Izquierda":
            self.costo += 2
            self.x[0] -= 1

        elif accion == "subir":
            self.costo += 3
            self.x[0] += 3

        elif accion == "bajar":
            self.costo += 3
            self.x[0] -= 3

        """
        Si estas en algunos de los pisos en los que es valido ir a la derecha, si le sumamos 1
        a la posicion, como va del 0 al 8, esto seria como moverse a la derecha, lo mismo
        aplica para la izquierda pero restando uno.
        Para subir y bajar solo se puede en las casillas 2, 5, 6 y 3, en las cuales si sumas
        o restas 3, caes en la casilla correspondiente, por ejemplo si estas en 2 y le sumas
        3, caes en 5, que es l casilla justo arriba. Y cuando la accion es nada, el costo no
        aumenta. Los costos son:
        Subir y bajar: 3
        izquierda y deracha: 2
        limpiar: 1
        nada: 0
        """

    def percepcion(self):
        robot = self.x[0]
        return self.x[0], self.x[robot + 1]


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Agente reactivo basado en modelo para el entorno de 9 cuartos.
    Sigue una estrategia para completar piso por piso.
    """
    def __init__(self):
        """
        Inicializa el modelo interno.
        Asumimos peor caso: todo sucio.
        """
        self.modelo = [0, 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        self.modelo[0] = robot
        self.modelo[robot + 1] = situacion

        if all(cuarto == 'limpio' for cuarto in self.modelo[1:]):
            return 'nada'

        if situacion == 'sucio':
            return 'limpiar'

        if robot == 0 or robot == 1:
            return 'ir_Derecha'

        elif robot == 2:
            return 'subir'

        elif robot == 5:
            if self.modelo[5] == 'sucio' or self.modelo[4] == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'subir'

        elif robot == 4:
            # Si el 3 (índice 4) no está limpio, sigo a la izquierda.
            if self.modelo[4] == 'sucio':
                return 'ir_Izquierda'
            else:
                return 'ir_Derecha'

        elif robot == 3:
            return 'ir_Derecha'

        elif robot == 8 or robot == 7:
            return 'ir_Izquierda'

        return 'nada'

def test():
    print("Prueba del entorno NueveCuartos con Agente Aleatorio")

    print("Prueba del entorno NueveCuartos con Agente Reactivo Modelo")
    entornos_o.simulador(NueveCuartos(),
                            AgenteReactivoModeloNueveCuartos(),
                            200)

if __name__ == "__main__":
    test()

