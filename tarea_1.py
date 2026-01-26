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
import random


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
            # No puedes ir a la derecha si ya estas en el borde derecho
            return robot not in [2, 5, 8]

        if accion == "ir_Izquierda":
            # No puedes ir a la izquierda si ya estas en el borde izquierdo
            return robot not in [0, 3, 6]

            # "limpiar" y "nada" siempre son legales
        return True

    def transicion(self, accion):

        robot = self.x[0]

        costo_accion = 0
        if accion == "limpiar":
            costo_accion = 1
        elif accion == "ir_Derecha" or accion == "ir_Izquierda":
            costo_accion = 2
        elif accion == "subir" or accion == "bajar":
            costo_accion = 3

        self.costo += costo_accion

        if not self.accion_legal(accion):
            return

        if accion == "limpiar":
            self.x[robot + 1] = "limpio"

        elif accion == "ir_Derecha":
            self.x[0] += 1

        elif accion == "ir_Izquierda":
            self.x[0] -= 1

        elif accion == "subir":
            self.x[0] += 3

        elif accion == "bajar":
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
        En una accion ilegal el costo es el de la accion pero el robot no hace nada.
        """

    def percepcion(self):
        robot = self.x[0]
        return self.x[0], self.x[robot + 1]


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un Agente reactivo basado en modelo para el entorno de 9 cuartos.
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

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales.
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)

class NueveCuartosCiego(NueveCuartos):
    """
    Entorno igual al de 9 cuartos, pero el robot no puede ver el estado del suelo.
    Solo sabe donde esta.
    """
    def percepcion(self):
        """
        Sobrescribe el metodo original.
        Devuelve solo la ubicacion del robot.
        """
        return self.x[0]


class AgenteReactivoModeloNueveCuartosCiego(AgenteReactivoModeloNueveCuartos):
    """
    Agente racional para entorno ciego.
    Como no ve la suciedad, limpia basándose en su modelo interno:
    'Si no recuerdo haber limpiado este cuarto, lo limpio y asumo que quedó bien'.
    """

    def programa(self, percepcion):
        robot = percepcion

        self.modelo[0] = robot

        if all(cuarto == 'limpio' for cuarto in self.modelo[1:]):
            return 'nada'

        estado_creido = self.modelo[robot + 1]

        if estado_creido == 'sucio':
            self.modelo[robot + 1] = 'limpio'
            return 'limpiar'

        # igual a la de nuevecuartos

        if robot == 0 or robot == 1:
            return 'ir_Derecha'
        elif robot == 2:
            return 'subir'

        elif robot == 5:
            if self.modelo[5] != 'limpio' or self.modelo[4] != 'limpio':
                return 'ir_Izquierda'
            else:
                return 'subir'
        elif robot == 4:
            if self.modelo[4] != 'limpio':
                return 'ir_Izquierda'
            else:
                return 'ir_Derecha'
        elif robot == 3:
            return 'ir_Derecha'

        elif robot == 8 or robot == 7:
            return 'ir_Izquierda'

        return 'nada'


class NueveCuartosEstocastico(NueveCuartos):
    """
    Entorno con incertidumbre (no se sabe si realizara la accion a ciencia cierta).
    """

    def transicion(self, accion):

        robot = self.x[0]

        costo_accion = 0
        if accion == "limpiar":
            costo_accion = 1
        elif accion in ["ir_Derecha", "ir_Izquierda"]:
            costo_accion = 2
        elif accion in ["subir", "bajar"]:
            costo_accion = 3

        self.costo += costo_accion

        if not self.accion_legal(accion):
            return

        rand = random.random()

        if accion == "limpiar":
            if rand <= 0.8:
                self.x[robot + 1] = "limpio"

        else:
            if rand <= 0.8:
                efecto = accion

            elif rand <= 0.9:
                return

            else:
                acciones_movimiento = ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]
                acciones_posibles = [a for a in acciones_movimiento if self.accion_legal(a)]
                efecto = random.choice(acciones_posibles)

            if efecto == "ir_Derecha":
                self.x[0] += 1
            elif efecto == "ir_Izquierda":
                self.x[0] -= 1
            elif efecto == "subir":
                self.x[0] += 3
            elif efecto == "bajar":
                self.x[0] -= 3

class AgenteReactivoModeloEstocastico(AgenteReactivoModeloNueveCuartos):
    """
    Agente racional para entorno estocástico.
    Hereda la logica del modelo nueve cuartos:
    """
    pass

def test():

    print("Prueba del entorno NueveCuartos con Agente Aleatorio")
    entornos_o.simulador(NueveCuartos(),
                         AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']),
                         200)

    print("Prueba del entorno NueveCuartos con Agente Reactivo Modelo")
    entornos_o.simulador(NueveCuartos(),
                            AgenteReactivoModeloNueveCuartos(),
                            200)

    """
    No hay comparacion entre este agente y el alateoreo, el alateoreo tiene un costo de entre 300 a 400 o mas
    en los primeros 200 pasos y ni si quiera cumple el objetivo de limpiar todos los cuartos, en cuanto
    al agente reactivo con modelo este termina en el menor costo posible, que seria 31.
    En este el programa sigue una ruta estilo serpiente, primero el primer piso, luego el segundo y por
    ultimo el tercero.
    """

    print("Prueba del entorno NueveCuartosCiego con Agente Reactivo Modelo Ciego")
    entornos_o.simulador(NueveCuartosCiego(),
                         AgenteReactivoModeloNueveCuartosCiego(),
                         200)

    """
    Esta es mas parecida al resultado de de AgenteReactivoModeloNueveCuartos, ya que hace lo mismo
    con la diferencia de que este agente limpia aunque el cuarto ya este limpio, pero despues de
    esto, lo guarda en su memoria y sigue avanzando.
    """

    print("Prueba del entorno NueveCuartosEstocastico con Agente Reactivo Modelo")
    entornos_o.simulador(NueveCuartosEstocastico(),
                         AgenteReactivoModeloEstocastico(),
                         200)

    """
    Esta se podria decir que es mas realista, a diferencia del alateoreo este se puede equivocar
    como podria pasar en la vida real, pero el costo sigue siendo muchisimo menos, no hay comparacion.
    """

if __name__ == "__main__":
    test()

