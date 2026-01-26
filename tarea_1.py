import entornos_o
from random import choice

class NueveCuartos(entornos_o.Entorno):
    def __init__(self, x0 = ["A"] + ["sucio"] * 9):
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
        self.modelo = ['A'] + ['sucio'] * 9

    def programa(self, percepcion):
        robot, situacion = percepcion

        self.modelo[' ABCDEFGHI'.find(robot)] = situacion

        if situacion == 'sucio':
            return 'limpiar'

        if all(s == 'limpio' for s in self.modelo[1:]):
            return 'nada'

        pasos = {'A': 'ir_Der', 'B': 'ir_Der', 'C': 'subir', 'F': 'ir_Izq',
                 'E': 'ir_Izq', 'D': 'subir', 'G': 'ir_Der', 'H': 'ir_Der', 'I': 'nada'}
        return pasos[robot]

def test():
    x0 = ["A"] + ["sucio"] * 9
    print("Simulación de 9 cuartos con Agente de Modelo")
    entornos_o.simulador(NueveCuartos(x0), AgenteReactivoModeloNueveCuartos(), 20)

    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteReactivoNueveCuartos(),
                         100)



if __name__ == "__main__":
    test()