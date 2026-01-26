import entornos_o
from random import choice
import random

"""
Los nueve cuartos se tomaron como :

        G  |  H  |  I
       ----|-----|----
        D  |  E  |  F
       ----|-----|----
        A  |  B  |  C
        
El robot comienza en el cuarto A con todos los cuartos sucios

Acciones legales:
Cuarto A : Ir_Derecha, Limpiar,Nada
Cuarto B : Ir_Izquierda, Ir_Derecha, Limpiar,Nada
Cuarto C : Ir_Izquierda, Subir, Limpiar,Nada
Cuarto D : Ir_Derecha, Bajar, Limpiar,Nada
Cuarto E : Ir_Izquierda, Ir_Derecha, Limpiar,Nada
Cuarto F : Ir_Izquierda, Subir, Limpiar,Nada
Cuarto G : Ir_Derecha, Bajar, Limpiar,Nada
Cuarto H : Ir_Izquierda, Ir_Derecha, Limpiar,Nada
Cuarto I : Ir_Izquierda, Limpiar,Nada
"""

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
            "D": {"ir_Der": "E", "bajar": "A"},
            "E": {"ir_Izq": "D", "ir_Der": "F"},
            "F": {"ir_Izq": "E", "subir": "I"},
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




class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
     Un agente Reactivo Modelo

     """

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
            'F': 'subir', 'I': 'ir_Izq', 'H': 'ir_Izq',
            'G': 'bajar', 'D': 'ir_Der', 'E': 'ir_Izq'
        }
        return pasos.get(robot, 'nada')


class AgenteNueveCuartosCiego(entornos_o.Agente):
    """
     Un agente ciego que no sabe si donde esta esta sucio o limpio
     """
    def __init__(self):
        self.plan = (
            ['limpiar', 'ir_Der'] * 2 + ['limpiar', 'subir'] *2 +
            ['limpiar', 'ir_Izq'] * 2 + ['limpiar', 'bajar'] +
            ['limpiar', 'ir_Der']  + ['limpiar', 'nada']
        )
        self.paso = 0

    def programa(self, _):
        if self.paso < len(self.plan):
            accion = self.plan[self.paso]
            self.paso += 1
            return accion
        acciones_ciegas=["nada"]
        return choice (acciones_ciegas)


class AgenteNueveCuartosEstocastico(entornos_o.Agente):

    """
     Un agente estocastico que toma algunas decisiones basadas en probabilidades
     """

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
            'F': 'subir', 'I': 'ir_Izq', 'H': 'ir_Izq',
            'G': 'bajar', 'D': 'ir_Der', 'E': 'ir_Izq'
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
    prueba_cuarto_sucio = ["A"] + ["sucio"] * 9
    prueba_cuarto_limpio = ["A"] + ["limpio"] * 9

    print("Simulación de 9 cuartos con Agente de Modelo")
    entornos_o.simulador(NueveCuartos(prueba_cuarto_sucio), AgenteReactivoModeloNueveCuartos(), 200)

    """
    Comparacion entre un agente Reactivo Modelo y un Agente Aleatorio
    Para cada agente se corrio la simulacion con 200 pasos

    Lo que se noto en la comparacion entre los agentes es que el agente reactivo cumplio con limpiar todos los cuartos 
    con un costo de 27 y al tener memoria y saber que termino de limpiar los cuartos se quedo en el ultimo cuarto haciendo nada 


    En cambio el agente aleatorio no logro limpiar todos los cuartos en los 200 pasos , y tuvo un costo mucho mayor de 148 sin cumplir el objetivo
    de limpiar todos los cuartos 

    """

    print("Simulación de 9 cuartos con Agente Aleatorio")
    entornos_o.simulador(NueveCuartos(prueba_cuarto_sucio), AgenteAleatorio  (["ir_Izq", "ir_Der", "subir", "bajar", "limpiar", "nada"]), 200)


    """
    Comparacion entre un agente aleatorio y un agente ciego
    Para cada agente se corrio la simulacion con 200 pasos
    
    El agente  ciego logro limpiar todos los cuartos con un costo de 27 , ya que aunque no tenga memoria , el sabe que en donde estaba estaba sucio lo
    limpiaba y asi hasta llegar al final, donde al no saber si el cuarto donde estaba estaba sucio o no , se quedo limpiandolo y moviendose sin sentido
    Y el agente aleatorio no logra limpiar todos los cuartos , y sigue haciendo cosas sin sentido 
    """

    print("Prueba del entorno con un Agente Ciego")
    entornos_o.simulador(NueveCuartos(prueba_cuarto_sucio),
                         AgenteNueveCuartosCiego(),
                        200)

    """
    Comparacion entre un agente estocastico y un agente aleatorio
    Para cada agente se corrio la simulacion con 200 pasos
    
    El agente estocastico si logro limpiar todos los cuartos con un costo de 30 , acercandose al reactivo modelo pero haciendo acciones 2 veces por
    como tiene configurada su probabilidad, pero en general logro limpiar todos los cuartos
    El agente aleatorio no logro limpiar todos los cuartos y seguia haciendo cosas sin sentido
    """

    print("Prueba del entorno con un Agente Estocastico")
    entornos_o.simulador(NueveCuartos(prueba_cuarto_sucio),
                         AgenteNueveCuartosEstocastico(),
                         200)

    """
    Prueba del agente ciego para verificar que funcione cuando estan todos los cuartos limpios , teniendo que limpiarlos todos a comparacion
    del agente modelo que puede saber si esta limpio o sucio
    """

    print ("Prueba entre el agente ciego y el basado en modelo para verificar el funcionamiento de ambos "
           "en la situacion de todos los cuartos limpios ")

    print("Prueba del entorno con un Agente basado en modelo")
    entornos_o.simulador(NueveCuartos(prueba_cuarto_limpio),
                         AgenteNueveCuartosCiego(),30)
    print("Prueba del entorno con un Agente basado en modelo")
    entornos_o.simulador(NueveCuartos(prueba_cuarto_limpio),
                         AgenteReactivoModeloNueveCuartos(),30)


if __name__ == "__main__":
    test()