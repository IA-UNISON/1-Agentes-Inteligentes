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
        acciones_ciegas=["limpiar","ir_Der","ir_Izq"]
        return choice (acciones_ciegas)


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


        if accion_planeada in ['ir_Der', 'ir_Izq']:
            prob = random.random()

            if prob <= 0.80:
                return accion_planeada

            elif 0.80 < prob <= 0.90:
                return 'nada'

            else:
                movimientos= {
                    'A': ['ir_Der'],
                    'B': ['ir_Der', 'ir_Izq'],
                    'C': ['ir_Izq', 'subir'],
                    'D': ['ir_Der',  'bajar'],
                    'E': ['ir_Der', 'ir_Izq'],
                    'F': ['ir_Izq', 'subir'],
                    'G': ['ir_Der', 'bajar'],
                    'H': ['ir_Der', 'ir_Izq'],
                    'I': ['ir_Izq']
                }

                movimientos_legales = movimientos.get(robot, [])

                acciones_totales = movimientos_legales + ['limpiar', 'nada']

                return random.choice(acciones_totales)
        return pasos.get(robot, 'nada')


def test():
    x0 = ["A"] + ["sucio"] * 9

    print("Prueba del entorno con un Agente Reactivo")
    entornos_o.simulador(NueveCuartos(x0),AgenteReactivoNueveCuartos(),  200)

    print("Simulación de 9 cuartos con Agente Aleatorio")
    entornos_o.simulador(NueveCuartos(x0), AgenteAleatorio  (["ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada"]), 200)

    """
    Comparacion entre un agente Reactivo y un Agente Aleatorio
    Para cada agente se corrio la simulacion con 200 pasos
    
    Lo que se noto en la comparacion entre los agentes es que el agente reactivo cumplio con limpiar todos los cuartos 
    con un costo de 27 pero al seguir corriendo la simulacion el agente se  quedo entre el cuarto I y H sin hacer nada mas
    llendo entre uno y el otro sabiendo que ya estaban limpio , el costo al final de la simulacion fue de 391
    
    En cambio el agente aleatorio no logro limpiar todos los cuartos , por que hacia cosas sin sentido como tomar la decision 
    de ir a la izquierda en un lado que no podia , o quedarse sin hacer nada en un cuarto sucio , 
    el costo final de la simulacion fue de 141 , siendo bastante menor que el del agente reactivo pero sin limpiar todos los cuartos
    
    """

    """
    Comparacion entre un agente aleatorio y un agente ciego
    Para cada agente se corrio la simulacion con 200 pasos
    
    El agente  ciego logro limpiar todos los cuartos con un costo de 27 , ya que aunque no tenga memoria , el sabe que en donde estaba estaba sucio lo
    limpiaba y asi hasta llegar al final, donde al no saber si el cuarto donde estaba estaba sucio o no , se quedo limpiandolo y moviendose sin sentido
    Y el agente aleatorio no logra limpiar todos los cuartos , y sigue haciendo cosas sin sentido 
    """

    print("Prueba del entorno con un Agente Ciego")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteNueveCuartosCiego(),
                        200)

    """
    Comparacion entre un agente estocastico y un agente aleatorio
    Para cada agente se corrio la simulacion con 200 pasos
    
    El agente estocastico si logro limpiar todos los cuartos con un costo de 33 , en un momento decidio no hacer nada en momentos que solo 
    debia de ir a la derecha o limpiar 2 veces por como se configuraron sus acciones con probabilidades , pero en general logro limpiar todos los cuartos
    El agente aleatorio no logro limpiar todos los cuartos y seguia haciendo cosas sin sentido
    """

    print("Prueba del entorno con un Agente Estocastico")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteNueveCuartosEstocastico(),
                         200)

    print("Simulación de 9 cuartos con Agente de Modelo")
    entornos_o.simulador(NueveCuartos(x0), AgenteReactivoModeloNueveCuartos(), 200)



if __name__ == "__main__":
    test()