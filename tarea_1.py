# -*- coding: utf-8 -*-
"""
Tarea 1 - Agentes Inteligentes (UNISON)
Aquí hice el entorno de 9 cuartos (3x3) y los agentes que pide la tarea.
La idea es comparar un agente aleatorio vs uno "más inteligente" en 200 pasos.

OJO: esto está comentado como alumno (o sea, no tan pro).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional
import random

# posición = (piso, cuarto)
# piso: 0,1,2
# cuarto: 0=izq, 1=medio, 2=der
Pos = Tuple[int, int]

# acciones permitidas (las que pide el pdf/README)
ACTIONS = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]


def idx(pos: Pos) -> int:
    """convierte (piso,cuarto) a indice 0..8 para guardar la suciedad en una lista"""
    piso, cuarto = pos
    return piso * 3 + cuarto


def clamp(x: int, lo: int, hi: int) -> int:
    """para que no se pase de 0..2"""
    return max(lo, min(hi, x))


@dataclass
class Percept:
    # lo que el agente "ve" cada paso
    pos: Pos
    sucio: Optional[bool]  # si es ciego, aquí va None


# ------------------------------
# Entorno normal (NueveCuartos)
# ------------------------------
class NueveCuartos:
    """
    9 cuartos (3 pisos x 3 cuartos).
    Reglas especiales:
      - subir solo desde cuarto derecho (2) y solo si piso < 2
      - bajar solo desde cuarto izquierdo (0) y solo si piso > 0

    Score: bonifica limpieza y castiga costos, y subir/bajar más caro.
    """

    COSTO = {
        "limpiar": 1,
        "ir_Derecha": 2,
        "ir_Izquierda": 2,
        "subir": 5,   # caro porque subir/bajar debe ser "más costoso"
        "bajar": 5,
        "nada": 1,
    }

    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)
        self.reset()

    def reset(self, suciedad_random: bool = True) -> Percept:
        # posición random del agente para arrancar
        self.pos: Pos = (self.rng.randint(0, 2), self.rng.randint(0, 2))

        # lista de 9 valores True/False: True = sucio
        if suciedad_random:
            self.sucio: List[bool] = [self.rng.random() < 0.5 for _ in range(9)]
        else:
            self.sucio = [True] * 9

        self.pasos = 0
        self.costo_total = 0
        return self.percept()

    def percept(self) -> Percept:
        # lo normal: sí puede ver si el cuarto actual está sucio
        return Percept(pos=self.pos, sucio=self.sucio[idx(self.pos)])

    def todos_limpios(self) -> bool:
        # si ningún cuarto está sucio
        return not any(self.sucio)

    def acciones_legales(self) -> List[str]:
        # acciones base
        piso, cuarto = self.pos
        leg = ["ir_Derecha", "ir_Izquierda", "limpiar", "nada"]

        # subir solo desde el cuarto derecho (2) y si no estás en el piso 2
        if piso < 2 and cuarto == 2:
            leg.append("subir")

        # bajar solo desde el cuarto izq (0) y si no estás en el piso 0
        if piso > 0 and cuarto == 0:
            leg.append("bajar")

        return leg

    def step(self, action: str) -> Percept:
        # si el agente manda algo raro, error
        if action not in ACTIONS:
            raise ValueError(f"Acción inválida: {action}")

        # si manda una acción ilegal, lo castigamos con "nada" (así no truena)
        if action not in self.acciones_legales():
            action = "nada"

        self.pasos += 1
        self.costo_total += self.COSTO[action]

        piso, cuarto = self.pos

        # movimientos laterales
        if action == "ir_Derecha":
            cuarto = clamp(cuarto + 1, 0, 2)
        elif action == "ir_Izquierda":
            cuarto = clamp(cuarto - 1, 0, 2)

        # movimientos verticales
        elif action == "subir":
            piso = clamp(piso + 1, 0, 2)
        elif action == "bajar":
            piso = clamp(piso - 1, 0, 2)

        # limpiar
        elif action == "limpiar":
            self.sucio[idx(self.pos)] = False

        # nada
        elif action == "nada":
            pass

        self.pos = (piso, cuarto)
        return self.percept()

    def score(self) -> float:
        """
        Score inventado pero cumple:
        - premia tener cuartos limpios
        - penaliza gastar costo (y subir/bajar cuesta más)
        """
        limpios = sum(1 for x in self.sucio if not x)
        bonus = 10 * limpios
        if self.todos_limpios():
            bonus += 1000
        return bonus - self.costo_total


# ------------------------------
# Entorno ciego (hereda)
# ------------------------------
class NueveCuartosCiego(NueveCuartos):
    """
    Igual pero no puede ver suciedad, solo sabe su posición.
    """

    def percept(self) -> Percept:
        return Percept(pos=self.pos, sucio=None)


# ------------------------------
# Entorno estocástico (hereda)
# ------------------------------
class NueveCuartosEstocastico(NueveCuartos):
    """
    Estocástico:
      - limpiar: 80% funciona, 20% falla
      - moverse: 80% hace lo pedido, 10% se queda, 10% hace algo legal random
    """

    def step(self, action: str) -> Percept:
        if action not in ACTIONS:
            raise ValueError(f"Acción inválida: {action}")

        if action not in self.acciones_legales():
            action = "nada"

        self.pasos += 1
        self.costo_total += self.COSTO[action]

        # si es limpiar, a veces no limpia
        if action == "limpiar":
            if self.rng.random() < 0.80:
                self.sucio[idx(self.pos)] = False
            return self.percept()

        # si es movimiento, a veces se equivoca
        if action in ("ir_Derecha", "ir_Izquierda", "subir", "bajar"):
            r = self.rng.random()
            if r < 0.80:
                # hace lo que pidió
                return super().step(action)
            elif r < 0.90:
                # se queda (pero ya pagó el costo)
                return self.percept()
            else:
                # hace una acción legal al azar
                alt = self.rng.choice(self.acciones_legales())
                return super().step(alt)

        return super().step(action)


# ------------------------------
# Agentes
# ------------------------------
class Agent:
    def act(self, percept: Percept) -> str:
        raise NotImplementedError


class RandomAgent(Agent):
    # el agente más menso: solo elige cualquier acción random
    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)

    def act(self, percept: Percept) -> str:
        return self.rng.choice(ACTIONS)


class ModelBasedReactiveAgent(Agent):
    """
    Reactivo basado en modelo (tipo: mantiene memoria)
    - guarda lo que cree de cada cuarto (sucio/limpio/desconocido)
    - si cree que aquí está sucio -> limpia
    - si no -> se mueve al cuarto sucio/desconocido más cercano (heurística simple)
    """
    def __init__(self):
        self.belief: List[Optional[bool]] = [None] * 9
        self.pos: Pos = (0, 0)

    def act(self, percept: Percept) -> str:
        self.pos = percept.pos
        if percept.sucio is not None:
            self.belief[idx(self.pos)] = percept.sucio

        # si está sucio aquí, limpiar
        if self.belief[idx(self.pos)] is True:
            self.belief[idx(self.pos)] = False
            return "limpiar"

        # buscar targets que sean sucios o desconocidos (para intentar limpiar todo)
        targets = [i for i, v in enumerate(self.belief) if v in (True, None)]
        if not targets:
            return "nada"

        # elegimos el más cercano, pero subir/bajar lo cuento como más caro
        piso, cuarto = self.pos
        best_i = None
        best_d = 10**9
        for i in targets:
            tp, tc = divmod(i, 3)
            d = abs(tc - cuarto) + 2 * abs(tp - piso)  # vertical pesa más
            if d < best_d:
                best_d = d
                best_i = i

        tp, tc = divmod(best_i, 3)

        # moverte hacia ese target
        if tc > cuarto:
            return "ir_Derecha"
        if tc < cuarto:
            return "ir_Izquierda"

        # ya está en la misma columna
        if tp > piso:
            # para subir ocupas estar en cuarto 2
            if cuarto < 2:
                return "ir_Derecha"
            return "subir"

        if tp < piso:
            # para bajar ocupas estar en cuarto 0
            if cuarto > 0:
                return "ir_Izquierda"
            return "bajar"

        return "nada"


class BlindRationalAgent(Agent):
    """
    Agente racional para el entorno ciego:
    como no puede ver suciedad, recorre todos los cuartos y siempre intenta limpiar.
    (aunque ya esté limpio, pues no sabe)
    """
    def __init__(self):
        self.plan: List[Pos] = [
            (0, 0), (0, 1), (0, 2),
            (1, 2), (1, 1), (1, 0),
            (2, 0), (2, 1), (2, 2),
        ]
        self.target_index = 0
        self.toca_limpiar = True

    def act(self, percept: Percept) -> str:
        pos = percept.pos
        target = self.plan[self.target_index]

        # si ya llegué, primero intento limpiar una vez
        if pos == target and self.toca_limpiar:
            self.toca_limpiar = False
            return "limpiar"

        # luego paso al siguiente target
        if pos == target and not self.toca_limpiar:
            self.toca_limpiar = True
            self.target_index = (self.target_index + 1) % len(self.plan)
            target = self.plan[self.target_index]

        # moverse hacia target
        piso, cuarto = pos
        tp, tc = target

        if tc > cuarto:
            return "ir_Derecha"
        if tc < cuarto:
            return "ir_Izquierda"

        if tp > piso:
            if cuarto < 2:
                return "ir_Derecha"
            return "subir"

        if tp < piso:
            if cuarto > 0:
                return "ir_Izquierda"
            return "bajar"

        return "nada"


class StochasticRationalAgent(Agent):
    """
    Para el estocástico:
    como limpiar puede fallar, cuando llega a limpiar hace 2 limpiezas seguidas
    para subir probabilidad de que sí quede limpio.
    """
    def __init__(self):
        self.inner = ModelBasedReactiveAgent()
        self.extra_clean = 0

    def act(self, percept: Percept) -> str:
        if self.extra_clean > 0:
            self.extra_clean -= 1
            return "limpiar"

        a = self.inner.act(percept)
        if a == "limpiar":
            self.extra_clean = 1  # limpieza extra
        return a


# ------------------------------
# correr simulaciones
# ------------------------------
def run_sim(env, agent: Agent, steps: int = 200) -> float:
    p = env.reset(suciedad_random=True)
    for _ in range(steps):
        a = agent.act(p)
        p = env.step(a)
    return env.score()


def compare(title: str, env_factory, agent_a: Agent, agent_b: Agent,
            trials: int = 30, steps: int = 200, seed: int = 123):
    rng = random.Random(seed)
    scores_a = []
    scores_b = []

    # hago varias corridas para sacar promedio (si no, sale muy random)
    for _ in range(trials):
        s = rng.randint(1, 10**9)
        # misma semilla para que ambos agentes vean el mismo mundo inicial
        env1 = env_factory(s)
        env2 = env_factory(s)
        scores_a.append(run_sim(env1, agent_a, steps))
        scores_b.append(run_sim(env2, agent_b, steps))

    def avg(xs): return sum(xs) / len(xs)

    print("\n" + "=" * 60)
    print(title)
    print(f"Trials={trials}, Steps={steps}")
    print(f"A) {agent_a.__class__.__name__} promedio score: {avg(scores_a):.2f}")
    print(f"B) {agent_b.__class__.__name__} promedio score: {avg(scores_b):.2f}")


if __name__ == "__main__":
    # 1) modelo-based vs random (entorno normal)
    compare(
        "Inciso 2) NueveCuartos: Modelo-based vs Aleatorio",
        env_factory=lambda s: NueveCuartos(seed=s),
        agent_a=ModelBasedReactiveAgent(),
        agent_b=RandomAgent(seed=999),
        trials=30,
        steps=200
    )

    # 2) entorno ciego + agente racional vs random
    compare(
        "Inciso 3) NueveCuartosCiego: Racional ciego vs Aleatorio",
        env_factory=lambda s: NueveCuartosCiego(seed=s),
        agent_a=BlindRationalAgent(),
        agent_b=RandomAgent(seed=888),
        trials=30,
        steps=200
    )

    # 3) entorno estocástico + agente racional vs random
    compare(
        "Inciso 4) NueveCuartosEstocastico: Racional estocástico vs Aleatorio",
        env_factory=lambda s: NueveCuartosEstocastico(seed=s),
        agent_a=StochasticRationalAgent(),
        agent_b=RandomAgent(seed=777),
        trials=30,
        steps=200
    )
