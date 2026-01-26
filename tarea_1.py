#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'joaquinsotelo'

import entornos_f
from random import choice, random, seed

#Lista con acciones posibles
ACCIONES = ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada" )

def idx(piso, col):
    return (piso - 1) * 3 + col

def acciones_legales(entorno, s):
    return [a for a in ACCIONES if entorno.accion_legal(s, a)]

#Entorno base para reutilizar codigo
class NueveCuartosBase(entornos_f.Entorno):
    COSTO = {
        "limpiar": 1,
        "ir_Derecha": 2,
        "ir_Izquierda": 2,
        "subir": 4,
        "bajar": 4,
        "nada": 1,
    }

    def accion_legal(self, s, a):
        if a not in ACCIONES:
            return False
        (piso, col) = s[0]
        if a == "ir_Derecha":   return col < 3
        if a == "ir_Izquierda": return col > 1
        if a == "subir":        return (piso in (1, 2)) and (col == 3)
        if a == "bajar":        return (piso in (2, 3)) and (col == 1)
        return True
    
    def _aplica_determinista(self, s, a):
        (piso, col) = s[0]
        cuartos = list(s[1:])

        if a == "limpiar":
            cuartos[idx(piso, col) - 1] = "limpio"
            return ((piso, col), *cuartos)

        if a == "ir_Derecha":
            return ((piso, col + 1), *cuartos)
        if a == "ir_Izquierda":
            return ((piso, col - 1), *cuartos)
        if a == "subir":
            return ((piso + 1, col), *cuartos)
        if a == "bajar":
            return ((piso - 1, col), *cuartos)

        return s
    
    def transicion(self, s, a):
        if not self.accion_legal(s, a):
            a = "nada"

        todo_limpio = all(x == "limpio" for x in s[1:])
        c_local = 0 if (todo_limpio and a == "nada") else self.COSTO.get(a, 1)

        return self._aplica_determinista(s, a), c_local

    def percepcion(self, s):
        (piso, col) = s[0]
        estado_actual = s[idx(piso, col)]
        return (s[0], estado_actual, acciones_legales(self, s))

    @staticmethod
    def inicial(pos=(1, 1), estado="sucio"):
        # Estado inicial por defecto: todo sucio, robot en (1,1)
        return (pos, *([estado] * 9))

class NueveCuartos(NueveCuartosBase):
    pass

class NueveCuartosCiego(NueveCuartosBase):
    def percepcion (self, s):
        return (s[0], acciones_legales(self, s))
    
class NueveCuartosEstocastico(NueveCuartosBase):
    def transicion(self, s, a):
        if not self.accion_legal(s, a):
            a = "nada"

        todo_limpio = all(x == "limpio" for x in s[1:])
        c_local = 0 if (todo_limpio and a == "nada") else self.COSTO.get(a, 1)

        if a == "limpiar":
            return (self._aplica_determinista(s, "limpiar"), c_local) if random() < 0.80 else (s, c_local)

        if a in ("ir_Derecha", "ir_Izquierda", "subir", "bajar"):
            r = random()
            if r < 0.80:
                return self._aplica_determinista(s, a), c_local
            if r < 0.90:
                return s, c_local
            legales = acciones_legales(self, s)
            otras = [x for x in legales if x != a] or ["nada"]
            a2 = choice(otras)
            c2 = 0 if (todo_limpio and a2 == "nada") else self.COSTO.get(a2, 1)
            return self._aplica_determinista(s, a2), c_local + c2

        return s, c_local 

class AgenteAleatorio(entornos_f.Agente):
    def programa(self, p):
        legales = p[-1]
        return choice(legales) if legales else "nada"

class AgenteModeloNueve(entornos_f.Agente):
    def __init__(self):
        self.m = {(p, c): "desconocido" for p in (1, 2, 3) for c in (1, 2, 3)}

    def _todo_limpio(self):
        return all(v == "limpio" for v in self.m.values())

    def _pendiente_en_piso(self, piso):
        return any(self.m[(piso, c)] != "limpio" for c in (1, 2, 3))

    def _elige(self, legales, *prefs):
        for a in prefs:
            if a in legales:
                return a
        return choice(legales) if legales else "nada"

    def programa(self, p):
        (pos, estado, legales) = p
        piso, col = pos

        self.m[(piso, col)] = estado

        if estado == "sucio":
            return self._elige(legales, "limpiar")

        if self._todo_limpio():
            return self._elige(legales, "nada")

        if piso == 1:
            if self._pendiente_en_piso(1) and col < 3:
                return self._elige(legales, "ir_Derecha")
            if col < 3:
                return self._elige(legales, "ir_Derecha")
            return self._elige(legales, "subir", "nada")

        if piso == 2:
            if self._pendiente_en_piso(2) and col > 1:
                return self._elige(legales, "ir_Izquierda")
            if col < 3:
                return self._elige(legales, "ir_Derecha")
            return self._elige(legales, "subir", "nada")

        if self._pendiente_en_piso(3) and col > 1:
            return self._elige(legales, "ir_Izquierda")
        return self._elige(legales, "nada")

class AgenteCiegoRacional(entornos_f.Agente):

    def __init__(self):
        self.limpiados = set()
        #Ruta fija para que llegue a cada cuarto
        self.plan = [
            (1, 1), (1, 2), (1, 3),
            (2, 3), (2, 2), (2, 1), (2, 2), (2, 3),
            (3, 3), (3, 2), (3, 1)
        ]
        self.i = 0

    def _elige(self, legales, *prefs):
        for a in prefs:
            if a in legales:
                return a
        return choice(legales) if legales else "nada"

    def programa(self, p):
        pos, legales = p
        piso, col = pos

        while self.i < len(self.plan) and self.plan[self.i] == pos and pos in self.limpiados:
            self.i += 1

        if self.i < len(self.plan) and self.plan[self.i] == pos and pos not in self.limpiados:
            if "limpiar" in legales:
                self.limpiados.add(pos)
                return "limpiar"

        if self.i >= len(self.plan):
            return self._elige(legales, "nada")

        objetivo = self.plan[self.i]
        op, oc = objetivo

        if op == piso:
            if oc > col:
                return self._elige(legales, "ir_Derecha")
            if oc < col:
                return self._elige(legales, "ir_Izquierda")
            return self._elige(legales, "nada")

        if op == piso + 1:
            if col < 3:
                return self._elige(legales, "ir_Derecha")
            return self._elige(legales, "subir")

        if op == piso - 1:
            if col > 1:
                return self._elige(legales, "ir_Izquierda")
            return self._elige(legales, "bajar")

        return self._elige(legales, "nada")

#Pruebas
def resultado(traza):
    a, s, c = traza[-1]
    limpios = sum(1 for x in s[1:] if x == "limpio")
    return c, limpios

def correr(entorno, agente, s0, T=200):
    traza = entornos_f.simulador(entorno, agente, s0, T=T)
    return resultado(traza)

#Imprime el reporte con los resultados
def reporte(titulo, racional, aleatorio):
    print("\n" + "=" * 70)
    print(titulo)
    print(f"Racional  -> costo={racional[0]}, limpios={racional[1]}/9")
    print(f"Aleatorio -> costo={aleatorio[0]}, limpios={aleatorio[1]}/9")
    print("=" * 70)


if __name__ == "__main__":
    seed(7)
    T = 200
    s0 = NueveCuartosBase.inicial()

    # Normal
    reporte("NueveCuartos (normal): Modelo vs Aleatorio",
            correr(NueveCuartos(), AgenteModeloNueve(), s0, T),
            correr(NueveCuartos(), AgenteAleatorio(), s0, T))

    # Ciego
    reporte("NueveCuartosCiego: Racional vs Aleatorio",
            correr(NueveCuartosCiego(), AgenteCiegoRacional(), s0, T),
            correr(NueveCuartosCiego(), AgenteAleatorio(), s0, T))

    # Estocástico
    reporte("NueveCuartosEstocastico: Racional vs Aleatorio",
            correr(NueveCuartosEstocastico(), AgenteModeloNueve(), s0, T),
            correr(NueveCuartosEstocastico(), AgenteAleatorio(), s0, T))                      


# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

