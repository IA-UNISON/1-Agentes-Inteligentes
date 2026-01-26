import entornos_o
from random import choice
import random

class NueveCuartos(entornos_o.Entorno):
    def __init__(self, x0 = ["A"] + ["limpio"] * 9):
        self.x = x0[:]
        self.costo = 0

    def accion_legal(self, accion):
        return accion in ("ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError(f"Acción {accion} no legal")

        robot = self.x[0]

        movimientos = {
            "A": {"ir_Der": "B"},
            "B": {"ir_Izq": "A", "ir_Der": "C"},
            "C": {"ir_Izq": "B", "subir": "F"},
            "D": {"ir_Der": "E", "subir": "G"},
            "E": {"ir_Izq": "D", "ir_Der": "F"},
            "F": {"ir_Izq": "E", "bajar": "C"},
            "G": {"ir_Der": "H", "bajar": "D"},
            "H": {"ir_Izq": "G", "ir_Der": "I"},
            "I": {"ir_Izq": "H"}
        }

        if accion == "limpiar":
            indice = " ABCDEFGHI".find(robot)
            self.x[indice] = "limpio"
            self.costo += 1

        elif accion in movimientos[robot]:
            self.x[0] = movimientos[robot][accion]

            if accion in ("ir_Izq", "ir_Der"):
                self.costo += 2

            elif accion in ("subir", "bajar"):
                self.costo += 3


    def percepcion(self):
        robot = self.x[0]
        indice = " ABCDEFGHI".find(robot)
        return robot, self.x[indice]

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)


class AgenteReactivoNueveCuartos(entornos_o.Agente):
    def programa(self, percepcion):
        robot, situacion = percepcion
        if situacion == 'sucio':
            return 'limpiar'

        return ('ir_Der' if robot in ('A', 'B') else
                'subir' if robot == 'C' else
                'ir_Izq' if robot in ('F', 'E') else
                'subir' if robot == 'D' else
                'ir_Der' if robot in ('G', 'H') else
                'ir_Izq')


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    def __init__(self):
        self.memoria = {k: 'desconocido' for k in 'ABCDEFGHI'}

    def programa(self, percepcion):
        robot, situacion = percepcion
        self.memoria[robot] = situacion

        if situacion == 'sucio':
            return 'limpiar'

        if all(estado == 'limpio' for estado in self.memoria.values()):
            return 'nada'

        pasos = {
            'A': 'ir_Der', 'B': 'ir_Der', 'C': 'subir',
            'F': 'ir_Izq', 'E': 'ir_Izq', 'D': 'subir',
            'G': 'ir_Der', 'H': 'ir_Der', 'I': 'nada'
        }
        return pasos.get(robot, 'nada')


class AgenteNueveCuartosCiego(entornos_o.Agente):
    def __init__(self):
        self.plan = (
            ['limpiar', 'ir_Der'] * 2 + ['limpiar', 'subir'] +
            ['limpiar', 'ir_Izq'] * 2 + ['limpiar', 'subir'] +
            ['limpiar', 'ir_Der'] * 2 + ['limpiar', 'nada']
        )
        self.paso = 0

    def programa(self, _):
        if self.paso < len(self.plan):
            accion = self.plan[self.paso]
            self.paso += 1
            return accion
        return 'nada'


class AgenteNueveCuartosEstocastico(entornos_o.Agente):
    def __init__(self):
        self.memoria = {k: 'desconocido' for k in 'ABCDEFGHI'}

    def programa(self, percepcion):
        robot, situacion = percepcion
        self.memoria[robot] = situacion

        if situacion == 'sucio':
            if random.random() < 0.80:
                return 'limpiar'
            else:
                return 'nada'

        if all(estado == 'limpio' for estado in self.memoria.values()):
            return 'nada'

        pasos = {
            'A': 'ir_Der', 'B': 'ir_Der', 'C': 'subir',
            'F': 'ir_Izq', 'E': 'ir_Izq', 'D': 'subir',
            'G': 'ir_Der', 'H': 'ir_Der', 'I': 'nada'
        }

        accion_planeada = pasos.get(robot, 'nada')


        if accion_planeada in ['ir_Der', 'ir_Izq', 'subir']:
            prob = random.random()

            if prob <= 0.80:
                return accion_planeada

            elif 0.80 < prob <= 0.90:
                return 'nada'

            else:
                movimientos= {
                    'A': ['ir_Der', 'subir'],
                    'B': ['ir_Der', 'ir_Izq', 'subir'],
                    'C': ['ir_Izq', 'subir'],
                    'D': ['ir_Der', 'subir', 'bajar'],
                    'E': ['ir_Der', 'ir_Izq', 'subir', 'bajar'],
                    'F': ['ir_Izq', 'subir', 'bajar'],
                    'G': ['ir_Der', 'bajar'],
                    'H': ['ir_Der', 'ir_Izq', 'bajar'],
                    'I': ['ir_Izq', 'bajar']
                }

                movimientos_legales = movimientos.get(robot, [])

                acciones_totales = movimientos_legales + ['limpiar', 'nada']

                return random.choice(acciones_totales)
        return 'nada'


def test():
    x0 = ["A"] + ["sucio"] * 9
    print("Simulación de 9 cuartos con Agente de Modelo")
    entornos_o.simulador(NueveCuartos(x0), AgenteReactivoModeloNueveCuartos(), 50)

    print("Simulación de 9 cuartos con Agente de Modelo")
    entornos_o.simulador(NueveCuartos(x0), AgenteAleatorio  (["ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada"]), 200)


    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteReactivoNueveCuartos(),
                         50)

    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteNueveCuartosCiego(),
                        50)


    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteNueveCuartosEstocastico(),
                         50)


if __name__ == "__main__":
    test()