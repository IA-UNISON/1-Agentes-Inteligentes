#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tarea_1.py
------------
Revisa el archivo README.md con las instrucciones de la tarea.
"""
__author__ = 'Rosario Rodolfo Luna Ortiz'

from entornos_o import Entorno, Agente
import random


# ============================
# Entorno NueveCuartos
# ============================
class NueveCuartos(Entorno):
    def __init__(self):
        super().__init__()

        self.pisos = 3
        self.cuartos_por_piso = 3

        self.posicion = (1, 1)

        self.estado = {}
        for piso in range(1, 4):
            for cuarto in range(1, 4):
                self.estado[(piso, cuarto)] = "sucio"

        self.desempeno = 0
        self.costo_total = 0

        self.costos = {
            "subir": 7,
            "bajar": 5,
            "ir_Derecha": 3,
            "ir_Izquierda": 3,
            "limpiar": 1,
            "nada": 0
        }

    def accion_legal(self, accion):
        piso, cuarto = self.posicion

        if accion in ["limpiar", "nada"]:
            return True
        if accion == "ir_Derecha":
            return cuarto < 3
        if accion == "ir_Izquierda":
            return cuarto > 1
        if accion == "subir":
            return piso < 3 and cuarto == 3
        if accion == "bajar":
            return piso > 1 and cuarto == 1
        return False

    def costo_accion(self, accion):
        return self.costos.get(accion, 0)

    def transicion(self, accion):
        if not self.accion_legal(accion):
            return

        costo = self.costo_accion(accion)
        self.costo_total += costo
        self.desempeno -= costo

        piso, cuarto = self.posicion

        if accion == "limpiar":
            if self.estado[(piso, cuarto)] == "sucio":
                self.estado[(piso, cuarto)] = "limpio"
                self.desempeno += 10

        elif accion == "ir_Derecha":
            self.posicion = (piso, cuarto + 1)

        elif accion == "ir_Izquierda":
            self.posicion = (piso, cuarto - 1)

        elif accion == "subir":
            self.posicion = (piso + 1, cuarto)

        elif accion == "bajar":
            self.posicion = (piso - 1, cuarto)

        elif accion == "nada":
            pass

    def percepcion(self):
        piso, cuarto = self.posicion
        return self.posicion, self.estado[(piso, cuarto)]


# ============================
# Agente Aleatorio
# ============================
class AgenteAleatorio(Agente):
    def __init__(self):
        self.acciones = [
            "ir_Derecha", "ir_Izquierda",
            "subir", "bajar",
            "limpiar", "nada"
        ]

    def programa(self, percepcion):
        return random.choice(self.acciones)


# ============================
# Agente Reactivo Basado en Modelo
# ============================
class AgenteReactivoModeloNueveCuartos(Agente):
    def __init__(self):
        self.modelo = {}
        for piso in range(1, 4):
            for cuarto in range(1, 4):
                self.modelo[(piso, cuarto)] = "sucio"

    def programa(self, percepcion):
        (piso, cuarto), situacion = percepcion
        self.modelo[(piso, cuarto)] = situacion

        if situacion == "sucio":
            return "limpiar"

        for (p, c), estado in self.modelo.items():
            if estado == "sucio":
                if p > piso and cuarto == 3:
                    return "subir"
                if p < piso and cuarto == 1:
                    return "bajar"
                if c > cuarto:
                    return "ir_Derecha"
                if c < cuarto:
                    return "ir_Izquierda"

        return "nada"


# ============================
# Entorno NueveCuartosCiego
# ============================
class NueveCuartosCiego(NueveCuartos):
    def percepcion(self):
        return self.posicion


# ============================
# Agente Racional para Ciego
# ============================
class AgenteRacionalCiego(Agente):
    def __init__(self):
        self.memoria = {}
        for piso in range(1, 4):
            for cuarto in range(1, 4):
                self.memoria[(piso, cuarto)] = "sucio"

    def programa(self, percepcion):
        piso, cuarto = percepcion

        if self.memoria[(piso, cuarto)] == "sucio":
            self.memoria[(piso, cuarto)] = "limpio"
            return "limpiar"

        for (p, c), estado in self.memoria.items():
            if estado == "sucio":
                if p > piso and cuarto == 3:
                    return "subir"
                if p < piso and cuarto == 1:
                    return "bajar"
                if c > cuarto:
                    return "ir_Derecha"
                if c < cuarto:
                    return "ir_Izquierda"

        return "nada"


# ============================
# Entorno NueveCuartosEstocástico
# ============================
class NueveCuartosEstocastico(NueveCuartos):
    def transicion(self, accion):
        if not self.accion_legal(accion):
            return

        piso, cuarto = self.posicion
        r = random.random()

        if accion == "limpiar":
            if r < 0.8:
                super().transicion(accion)
            else:
                # Falló limpiar: se cobra costo, pero no se limpia
                costo = self.costo_accion(accion)
                self.costo_total += costo
                self.desempeno -= costo

        elif accion in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]:
            if r < 0.8:
                super().transicion(accion)
            elif r < 0.9:
                # Se queda en su lugar pero paga costo
                costo = self.costo_accion(accion)
                self.costo_total += costo
                self.desempeno -= costo
            else:
                acciones_legales = [
                    a for a in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]
                    if self.accion_legal(a)
                ]
                if acciones_legales:
                    super().transicion(random.choice(acciones_legales))
 


# ============================
# Agente Racional Estocástico
# ============================
class AgenteRacionalEstocastico(Agente):
    def __init__(self):
        self.modelo = {}
        for piso in range(1, 4):
            for cuarto in range(1, 4):
                self.modelo[(piso, cuarto)] = "sucio"

    def programa(self, percepcion):
        (piso, cuarto), situacion = percepcion
        self.modelo[(piso, cuarto)] = situacion

        if situacion == "sucio":
            return "limpiar"

        for (p, c), estado in self.modelo.items():
            if estado == "sucio":
                if p > piso and cuarto == 3:
                    return "subir"
                if p < piso and cuarto == 1:
                    return "bajar"
                if c > cuarto:
                    return "ir_Derecha"
                if c < cuarto:
                    return "ir_Izquierda"

        return "nada"


# ============================
# Simulación
# ============================
def simular_agente(entorno, agente, pasos=200):
    for _ in range(pasos):
        p = entorno.percepcion()
        accion = agente.programa(p)
        if entorno.accion_legal(accion):
            entorno.transicion(accion)

    print("Costo total:", entorno.costo_total)
    print("Desempeño:", entorno.desempeno)


# ============================
# Comparaciones
# ============================
def comparar_agentes():
    print("\n--- NueveCuartos Normal ---")
    simular_agente(NueveCuartos(), AgenteAleatorio())
    simular_agente(NueveCuartos(), AgenteReactivoModeloNueveCuartos())


def comparar_agentes_ciego():
    print("\n--- NueveCuartosCiego ---")
    simular_agente(NueveCuartosCiego(), AgenteAleatorio())
    simular_agente(NueveCuartosCiego(), AgenteRacionalCiego())


def comparar_agentes_estocastico():
    print("\n--- NueveCuartosEstocástico ---")
    simular_agente(NueveCuartosEstocastico(), AgenteAleatorio())
    simular_agente(NueveCuartosEstocastico(), AgenteRacionalEstocastico())


# ============================
# Main
# ============================
if __name__ == "__main__":
    comparar_agentes()
    comparar_agentes_ciego()
    comparar_agentes_estocastico()
