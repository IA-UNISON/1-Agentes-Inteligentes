#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'DanielEduardoAlvarezTerrazas'

import entornos_o
from random import choice, random

"""
Estructura de los 9 cuartos:

    Piso 3:  3A -- 3B -- 3C
             ↓           ⬆
    Piso 2:  2A -- 2B -- 2C
             ↓           ⬆   
    Piso 1:  1A -- 1B -- 1C
"""

# Lista de cuartos 
CUARTOS = ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"]


class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos distribuidos en 3 pisos.

    El estado se define como:
    [robot, 1A, 1B, 1C, 2A, 2B, 2C, 3A, 3B, 3C]
    
    donde el robot puede estar en cualquiera de los 9 cuartos: "1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"
    y cada cuarto puede ser "L" o "S" (L = Limpio, S = Sucio)

    Acciones válidas: ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    
    - ir_Derecha: A->B, B->C (en cualquier piso)
    - ir_Izquierda: A<-B, B<-C (en cualquier piso)
    - subir: solo legal en 1C y 2C
    - bajar: solo legal en 2A y 3A

    Costos:
    - limpiar: 1
    - ir_Derecha, ir_Izquierda: 2
    - subir, bajar: 3
    - nada: 0 si todo está limpio, 1 si hay algo sucio
    """

    def __init__(self, x0=["1A", "S", "S", "S", "S", "S", "S", "S", "S", "S"]):
        """
        Por default el robot está en 1A y todos los cuartos están sucios
        """
        self.x = x0[:]
        self.costo = 0

    def accion_legal(self, accion):
        """
        Verifica si una acción es legal en el estado actual
        """
        robot = self.x[0]
        piso = robot[0]  # '1', '2' o '3'
        cuarto = robot[1]  # 'A', 'B' o 'C'

        if accion == "ir_Derecha":
            return cuarto in ("A", "B")
        elif accion == "ir_Izquierda":
            return cuarto in ("B", "C")
        elif accion == "subir":
            return piso in ("1", "2") and cuarto == "C"
        elif accion == "bajar":
            return piso in ("2", "3") and cuarto == "A"
        elif accion in ("limpiar", "nada"):
            return True
        return False

    def transicion(self, accion):
        """
        Realiza la transición del estado según la acción.
        Si la acción no es legal, el agente permanece en su lugar y no ocurre ningún cambio.
        """
        robot = self.x[0]
        piso = robot[0]
        cuarto = robot[1]

        # Verificar si hay cuartos sucios
        hay_S = any(self.x[i] == "S" for i in range(1, 10))

        # Si la acción no es legal, el agente permanece en su lugar y no ocurre ningún cambio
        if not self.accion_legal(accion):
            if hay_S:
                self.costo += 1
            return

        # Calcular costo según la acción
        if accion == "nada":
            if hay_S:
                self.costo += 1
        elif accion == "limpiar":
            self.costo += 1
        elif accion in ("ir_Derecha", "ir_Izquierda"):
            self.costo += 2
        elif accion in ("subir", "bajar"):
            self.costo += 3

        # Ejecutar la acción
        if accion == "limpiar":
            idx = CUARTOS.index(robot) + 1
            self.x[idx] = "L"
        elif accion == "ir_Derecha":
            nuevo_cuarto = "B" if cuarto == "A" else "C"
            self.x[0] = piso + nuevo_cuarto
        elif accion == "ir_Izquierda":
            nuevo_cuarto = "A" if cuarto == "B" else "B"
            self.x[0] = piso + nuevo_cuarto
        elif accion == "subir":
            nuevo_piso = "2" if piso == "1" else "3"
            self.x[0] = nuevo_piso + cuarto
        elif accion == "bajar":
            nuevo_piso = "1" if piso == "2" else "2"
            self.x[0] = nuevo_piso + cuarto

    def percepcion(self):
        """
        Regresa donde está el robot y si el cuarto actual está S o L 
        como una tupla (robot, estado_cuarto_actual)
        """
        robot = self.x[0]
        idx = CUARTOS.index(robot) + 1
        return robot, self.x[idx]


class AgenteAleatorioNueveCuartos(entornos_o.Agente):
    """
    Un agente que solo regresa una acción al azar entre las acciones legales
    """
    def __init__(self):
        self.acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Agente reactivo basado en modelo para NueveCuartos.
    
    Mantiene un modelo interno del estado de todos los cuartos.
    Estrategia: Limpiar si está sucio, si no, ir recorriendo todos los cuartos 
    hasta encontrar uno sucio.
    """

    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ["1A", "S", "S", "S", "S", "S", "S", "S", "S", "S"]

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        idx = CUARTOS.index(robot) + 1
        self.modelo[idx] = situacion

        # Si todos los cuartos están limpios, no hacer nada
        if all(self.modelo[i] == "L" for i in range(1, 10)):
            return "nada"

        # Si el cuarto actual está sucio, limpiar
        if situacion == "S":
            return "limpiar"

        # Buscar el próximo cuarto sucio
        for cuarto in CUARTOS:
            idx_cuarto = CUARTOS.index(cuarto) + 1
            if self.modelo[idx_cuarto] == "S":
                return self._ir_hacia(robot, cuarto)

        # Si no hay cuartos sucios conocidos, seguir explorando
        return self._siguiente_movimiento(robot)

    def _ir_hacia(self, actual, destino):
        """
        Retorna la acción para ir del cuarto actual hacia el destino
        """
        piso_actual = actual[0]
        cuarto_actual = actual[1]
        piso_destino = destino[0]
        cuarto_destino = destino[1]

        if piso_actual < piso_destino:
            if cuarto_actual != "C":
                return "ir_Derecha"
            return "subir"
        elif piso_actual > piso_destino:
            if cuarto_actual != "A":
                return "ir_Izquierda"
            return "bajar"
        else:
            if cuarto_actual < cuarto_destino:
                return "ir_Derecha"
            elif cuarto_actual > cuarto_destino:
                return "ir_Izquierda"

        return "nada"

    def _siguiente_movimiento(self, robot):
        """
        Movimiento por defecto cuando no hay cuartos sucios conocidos
        """
        piso = robot[0]
        cuarto = robot[1]

        if cuarto == "C" and piso in ("1", "2"):
            return "subir"
        elif cuarto == "A" and piso in ("2", "3"):
            return "bajar"
        elif cuarto in ("A", "B"):
            return "ir_Derecha"
        else:
            return "ir_Izquierda"


class NueveCuartosCiego(NueveCuartos):
    """
    Igual que NueveCuartos, pero el agente solo sabe en qué cuarto está,
    no sabe si está L o S.
    """

    def percepcion(self):
        """
        Solo retorna la ubicación del robot, no el estado de limpieza
        """
        return self.x[0]


class AgenteReactivoModeloNueveCuartosCiego(AgenteReactivoModeloNueveCuartos):
    """
    Agente reactivo basado en modelo para NueveCuartosCiego.
    
    Como no puede ver si un cuarto está sucio, debe recorrer todos
    los cuartos y limpiarlos por si acaso, manteniendo un modelo
    interno de lo que ha limpiado.
    """

    def __init__(self):
        """
        Inicializa el modelo interno asumiendo todos sucios
        """
        self.modelo = ["?", "S", "S", "S", "S", "S", "S", "S", "S", "S"]

    def programa(self, percepcion):
        robot = percepcion  # Solo recibe la ubicación

        # Actualizar posición en el modelo
        self.modelo[0] = robot
        idx = CUARTOS.index(robot) + 1

        # Si todos los cuartos ya fueron limpiados según el modelo, no hacer nada
        if all(self.modelo[i] == "L" for i in range(1, 10)):
            return "nada"

        # Si el cuarto actual no ha sido limpiado, limpiar
        if self.modelo[idx] == "S":
            self.modelo[idx] = "L"
            return "limpiar"

        # Buscar el próximo cuarto que no ha sido limpiado
        for cuarto in CUARTOS:
            idx_cuarto = CUARTOS.index(cuarto) + 1
            if self.modelo[idx_cuarto] == "S":
                return self._ir_hacia(robot, cuarto)

        return "nada"


class NueveCuartosEstocastico(NueveCuartos):
    """
    Igual que NueveCuartos pero con comportamiento estocástico:
    
    - Limpiar: 80% de las veces limpia, 20% deja sucio
    - Moverse: 80% se mueve correctamente, 10% se queda, 10% acción legal aleatoria
    """

    def _obtener_acciones_legales(self):
        """
        Retorna lista de acciones legales en el estado actual
        """
        acciones = ["limpiar", "nada"]
        robot = self.x[0]
        piso = robot[0]
        cuarto = robot[1]

        if cuarto in ("A", "B"):
            acciones.append("ir_Derecha")
        if cuarto in ("B", "C"):
            acciones.append("ir_Izquierda")
        if piso in ("1", "2") and cuarto == "C":
            acciones.append("subir")
        if piso in ("2", "3") and cuarto == "A":
            acciones.append("bajar")

        return acciones

    def transicion(self, accion):
        """
        Realiza la transición con comportamiento estocástico.
        Si la acción no es legal, el agente permanece en su lugar y no ocurre ningún cambio.
        """
        robot = self.x[0]
        piso = robot[0]
        cuarto = robot[1]

        # Verificar si hay cuartos sucios
        hay_S = any(self.x[i] == "S" for i in range(1, 10))

        # Si la acción no es legal, el agente permanece en su lugar y no ocurre ningún cambio
        if not self.accion_legal(accion):
            if hay_S:
                self.costo += 1
            return

        # Calcular costo según la acción
        if accion == "nada":
            if hay_S:
                self.costo += 1
        elif accion == "limpiar":
            self.costo += 1
        elif accion in ("ir_Derecha", "ir_Izquierda"):
            self.costo += 2
        elif accion in ("subir", "bajar"):
            self.costo += 3

        # Ejecutar la acción con estocasticidad
        if accion == "limpiar":
            # 80% limpia, 20% deja sucio
            if random() < 0.8:
                idx = CUARTOS.index(robot) + 1
                self.x[idx] = "L"
            # Si no, el cuarto queda como esta

        elif accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar"):
            # 80% se mueve correctamente, 10% se queda, 10% acción aleatoria
            r = random()
            if r < 0.8:
                # Movimiento correcto
                self._ejecutar_movimiento(accion)
            elif r < 0.9:
                # Se queda en su lugar
                pass
            else:
                # Acción legal aleatoria
                acciones_legales = self._obtener_acciones_legales()
                accion_aleatoria = choice(acciones_legales)
                if accion_aleatoria == "limpiar":
                    idx = CUARTOS.index(robot) + 1
                    self.x[idx] = "L"
                elif accion_aleatoria in ("ir_Derecha", "ir_Izquierda", "subir", "bajar"):
                    self._ejecutar_movimiento(accion_aleatoria)

    def _ejecutar_movimiento(self, accion):
        """
        Ejecuta un movimiento sin estocasticidad
        """
        robot = self.x[0]
        piso = robot[0]
        cuarto = robot[1]

        if accion == "ir_Derecha":
            nuevo_cuarto = "B" if cuarto == "A" else "C"
            self.x[0] = piso + nuevo_cuarto
        elif accion == "ir_Izquierda":
            nuevo_cuarto = "A" if cuarto == "B" else "B"
            self.x[0] = piso + nuevo_cuarto
        elif accion == "subir":
            nuevo_piso = "2" if piso == "1" else "3"
            self.x[0] = nuevo_piso + cuarto
        elif accion == "bajar":
            nuevo_piso = "1" if piso == "2" else "2"
            self.x[0] = nuevo_piso + cuarto


def test():
    """
    Prueba del entorno y los agentes
    """

    x0 = ["1A", "S", "S", "S", "S", "S", "S", "S", "S", "S"]

    print("Agente Aleatorio")
    _, _, costos_aleatorio = entornos_o.simulador(
        NueveCuartos(x0),
        AgenteAleatorioNueveCuartos(),
        200,
        verbose=True
    )

    print("prueba del agente reactivo basado en modelo")
    _, _, costos_modelo = entornos_o.simulador(
        NueveCuartos(x0),
        AgenteReactivoModeloNueveCuartos(),
        200,
        verbose=True
    )

    print("prueba del agente aleatorio en entorno ciego")
    _, _, costos_ciego_aleatorio = entornos_o.simulador(
        NueveCuartosCiego(x0),
        AgenteAleatorioNueveCuartos(),
        200,
        verbose=True
    )

    print("prueba del agente reactivo con modelo en entorno ciego")
    _, _, costos_ciego_modelo = entornos_o.simulador(
        NueveCuartosCiego(x0),
        AgenteReactivoModeloNueveCuartosCiego(),
        200,
        verbose=True
    )

    print("prueba del agente aleatorio en entorno estocástico")
    _, _, costos_est_aleatorio = entornos_o.simulador(
        NueveCuartosEstocastico(x0),
        AgenteAleatorioNueveCuartos(),
        200,
        verbose=True
    )

    print("prueba del agente reactivo con modelo en entorno estocástico")
    _, _, costos_est_modelo = entornos_o.simulador(
        NueveCuartosEstocastico(x0),
        AgenteReactivoModeloNueveCuartos(),
        200,
        verbose=True
    )

    print("\n" + "=" * 90)
    print("RESUMEN DE COMPARACIONES")
    print("=" * 90)
    print("NueveCuartos:")
    print(f"  Agente Aleatorio: {costos_aleatorio[-1]}")
    print(f"  Agente Modelo:    {costos_modelo[-1]}")
    print(f"  Mejora:           {costos_aleatorio[-1] - costos_modelo[-1]} puntos de costo")

    print("NueveCuartosCiego:")
    print(f"  Agente Aleatorio: {costos_ciego_aleatorio[-1]}")
    print(f"  Agente Modelo:    {costos_ciego_modelo[-1]}")
    print(f"  Mejora:           {costos_ciego_aleatorio[-1] - costos_ciego_modelo[-1]} puntos de costo")

    print("NueveCuartosEstocastico:")
    print(f"  Agente Aleatorio: {costos_est_aleatorio[-1]}")
    print(f"  Agente Modelo:    {costos_est_modelo[-1]}")
    print(f"  Mejora:           {costos_est_aleatorio[-1] - costos_est_modelo[-1]} puntos de costo")

if __name__ == "__main__":
    test()

#Al realizar las pruebas, se puede observar que el agente reactivo basado en modelo es mejor que el agente aleatorio en todos los casos.
#Esto se debe a que el agente reactivo basado en modelo sigue una estrategia de limpiar si está sucio, si no, ir recorriendo todos los cuartos hasta encontrar uno sucio.
#El agente aleatorio, por otro lado, solo puede actuar de manera aleatoria y no tiene una estrategia para limpiar los cuartos.