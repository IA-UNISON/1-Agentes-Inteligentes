
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Diego Gallegos Hernandez'

import entornos_o
import random

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos en una cuadricula 3x3.

    El estado se define como: (robot, 0, 1, 2, ..., 8) 
    donde robot puede tener los valores "0", "1", ....
    y los cuartos representados por numeros pueden ser "limpio" o "sucio"
    
    Las acciones validas en el entorno son
    ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    Donde subir solo es posible en los cuartos de la derecha, en los 
    primeros dos pisos, y bajar solo en los cuartos de la izquierda, en
    los dos ultimos pisos.
    Ir a la derecha y a la izquierda no son legales en todos los casos.
    
    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    
    def __init__(self, x0 = [0, "sucio", "sucio", "sucio", 
                                "sucio", "sucio", "sucio", 
                                "sucio", "sucio", "sucio",]):
        """
        El robot por default comienza en 0 y 
        todos los cuartos estan sucios.
        """
        self.x = x0[:]
        self.costo = 0
    
    def accion_legal(self, accion):
        """
        ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
        """
        if accion == "subir":
            return True if self.x[0] in (2, 5) else False
        elif accion == "bajar":
            return True if self.x[0] in (6, 3) else False
        elif accion == "ir_Derecha":
            return True if self.x[0] not in (2, 5, 8) else False
        elif accion == "ir_Izquierda":
            return True if self.x[0] not in (0, 3, 6) else False
        
        return accion in ("limpiar", "nada")
        
    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")
        
        nuevo_estado = self.x[:]
        robot = nuevo_estado[0]
        
        if accion == "ir_Derecha":
            robot += 1
            nuevo_estado[0] = robot
            self.costo += 2
        elif accion == "ir_Izquierda":
            robot -= 1
            nuevo_estado[0] = robot
            self.costo += 2
        elif accion == "subir":
            robot += 3
            nuevo_estado[0] = robot
            self.costo += 3
        elif accion == "bajar":
            robot -= 3
            nuevo_estado[0] = robot
            self.costo += 3
        elif accion == "limpiar":
            cuarto = robot
            nuevo_estado[cuarto + 1] = "limpio"
            self.costo += 1
        elif accion == "nada":
            if any(self.x[i] == "sucio" for i in range(1, 10)):
                self.costo += 1
        
        self.x = nuevo_estado
    
    def percepcion(self):
        robot = self.x[0]
        estado = self.x[robot + 1]
        return robot, estado
    
class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo. Conserva memoria de su entorno.
    """
    
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = [0, "sucio", "sucio", "sucio", 
                          "sucio", "sucio", "sucio", 
                          "sucio", "sucio", "sucio",]
        
    def programa(self, percepcion):
        robot, situacion = percepcion 
    
        self.modelo[0] = robot
        self.modelo[robot + 1] = situacion
    
        if situacion == "sucio":
            return "limpiar"
    
        objetivo = None
        for i, estado in enumerate(self.modelo[1:]):
            if estado == "sucio":
                objetivo = i
                break

        if objetivo is not None and objetivo > robot:
            if robot in (2, 5):
                return "subir"
            else: 
                return "ir_Derecha"

        if objetivo is not None and objetivo < robot:
            if robot in (6, 3):
                return "bajar"
            else:
                return "ir_Izquierda"
        
        if all(cuarto == "limpio" for cuarto in self.modelo[1:]):
            return "nada"
    
        # exploración
        if robot in (2, 5):
            return random.choice(["ir_Izquierda", "subir"])
        elif robot in (6, 3):
            return random.choice(["ir_Derecha", "bajar"])
        elif robot in (1, 4, 7): 
            return random.choice(["ir_Derecha", "ir_Izquierda"])
        elif robot == 0:
            return "ir_Derecha"
        elif robot == 8:
            return "ir_Izquierda"

        return "nada"
    
class AgenteAleatorioNueveCuartos(entornos_o.Agente):
    """
    Un agente que selecciona acciones aleatorias entre las acciones legales
    """
    
    def __init__(self):
        self.acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    
    def programa(self, percepcion):
        """
        Selecciona una acción aleatoria solo entre las acciones válidas
        para la posición actual del robot
        """
        robot, _ = percepcion
        
        acciones_validas = []
        
        for accion in self.acciones:
            if accion == "subir" and robot in (2, 5):
                acciones_validas.append(accion)
            elif accion == "bajar" and robot in (6, 3):
                acciones_validas.append(accion)
            elif accion == "ir_Derecha" and robot not in (2, 5, 8):
                acciones_validas.append(accion)
            elif accion == "ir_Izquierda" and robot not in (0, 3, 6):
                acciones_validas.append(accion)
            elif accion in ("limpiar", "nada"):
                acciones_validas.append(accion)
        
        return random.choice(acciones_validas)
    
class NueveCuartosCiego(NueveCuartos):
    """
    Igual que NueveCuartos, pero el agente no puede ver 
    si el cuarto está limpio o sucio
    """
    
    def percepcion(self):
        """
        Solo regresa la posición del robot
        """
        robot = self.x[0]
        return robot,  
    
class AgenteReactivoModeloNueveCuartosCiego(entornos_o.Agente):
    """
    Agente reactivo basado en modelo para entorno ciego.
    No puede ver si los cuartos están limpios, solo su posición.
    """
    
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = [0, "sucio", "sucio", "sucio",
                          "sucio", "sucio", "sucio",
                          "sucio", "sucio", "sucio"]
        self.visitados = set()  
    
    def programa(self, percepcion):
        robot, = percepcion  
        
        self.modelo[0] = robot
        
        if robot not in self.visitados:
            self.visitados.add(robot)
            self.modelo[robot + 1] = "limpio"
            return "limpiar"
        
        if len(self.visitados) == 9:
            return "nada"
        
        objetivo = None
        for i in range(9):
            if i not in self.visitados:
                objetivo = i
                break
        
        if objetivo is not None:
            if objetivo > robot:
                if robot in (2, 5):
                    return "subir"
                else:
                    return "ir_Derecha"
            
            elif objetivo < robot:
                if robot in (6, 3):
                    return "bajar"
                else:
                    return "ir_Izquierda"
        
        if robot == 0:
            return "ir_Derecha"
        elif robot == 1:
            return "ir_Derecha"
        elif robot == 2:
            return "subir"
        elif robot == 3:
            return "ir_Derecha"
        elif robot == 4:
            return "ir_Derecha"
        elif robot == 5:
            return "subir"
        elif robot == 6:
            return "ir_Derecha"
        elif robot == 7:
            return "ir_Derecha"
        elif robot == 8:
            return "nada"
        
        return "nada"
    
class AgenteAleatorioNueveCuartosCiego(entornos_o.Agente):
    """
    Un agente que selecciona acciones aleatorias entre las acciones legales
    para el entorno ciego (donde solo percibe su posición)
    """
    
    def __init__(self):
        self.acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    
    def programa(self, percepcion):
        """
        Selecciona una acción aleatoria solo entre las acciones válidas
        para la posición actual del robot
        """
        robot, = percepcion  
        
        acciones_validas = []
        
        for accion in self.acciones:
            if accion == "subir" and robot in (2, 5):
                acciones_validas.append(accion)
            elif accion == "bajar" and robot in (6, 3):
                acciones_validas.append(accion)
            elif accion == "ir_Derecha" and robot not in (2, 5, 8):
                acciones_validas.append(accion)
            elif accion == "ir_Izquierda" and robot not in (0, 3, 6):
                acciones_validas.append(accion)
            elif accion in ("limpiar", "nada"):
                acciones_validas.append(accion)
        
        return random.choice(acciones_validas)
    
class NueveCuartosEstocastico(NueveCuartos):
    """
    Entorno estocástico donde las acciones no siempre funcionan como se espera:
    - Limpiar: 80% limpia, 20% no hace nada
    - Moverse: 80% se mueve correctamente, 10% se queda en su lugar, 10% acción legal aleatoria
    """
    
    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")
        
        robot = self.x[0]
        
        if accion == "limpiar":
            probabilidad = random.random()
            if probabilidad < 0.8: 
                self.x[robot + 1] = "limpio"
            self.costo += 1
            return
        
        if accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar"):
            probabilidad = random.random()
            
            if probabilidad < 0.8:  
                accion_ejecutada = accion
            elif probabilidad < 0.9: 
                accion_ejecutada = "nada"
            else:  
                acciones_legales = []
                if robot in (2, 5):
                    acciones_legales.append("subir")
                if robot in (6, 3):
                    acciones_legales.append("bajar")
                if robot not in (2, 5, 8):
                    acciones_legales.append("ir_Derecha")
                if robot not in (0, 3, 6):
                    acciones_legales.append("ir_Izquierda")
                acciones_legales.extend(["limpiar", "nada"])
                
                accion_ejecutada = random.choice(acciones_legales)
            
            if accion_ejecutada == "ir_Derecha":
                self.x[0] += 1
                self.costo += 2
            elif accion_ejecutada == "ir_Izquierda":
                self.x[0] -= 1
                self.costo += 2
            elif accion_ejecutada == "subir":
                self.x[0] += 3
                self.costo += 3
            elif accion_ejecutada == "bajar":
                self.x[0] -= 3
                self.costo += 3
            elif accion_ejecutada == "limpiar":
                if random.random() < 0.8:
                    self.x[self.x[0] + 1] = "limpio"
                self.costo += 1
            elif accion_ejecutada == "nada":
                if any(self.x[i] == "sucio" for i in range(1, 10)):
                    self.costo += 1
        
        elif accion == "nada":
            if any(self.x[i] == "sucio" for i in range(1, 10)):
                self.costo += 1


class AgenteReactivoModeloNueveCuartosEstocastico(entornos_o.Agente):
    """
    Agente reactivo basado en modelo para entorno estocástico.
    Mantiene un modelo interno del estado de los cuartos.
    """
    
    def __init__(self):
        """
        Inicializa el modelo interno asumiendo todos los cuartos sucios
        """
        self.modelo = [0, "sucio", "sucio", "sucio",
                          "sucio", "sucio", "sucio",
                          "sucio", "sucio", "sucio"]
    
    def programa(self, percepcion):
        robot, situacion = percepcion
        
        self.modelo[0] = robot
        self.modelo[robot + 1] = situacion
        
        if situacion == "sucio":
            return "limpiar"
        
        objetivo = None
        for i, estado in enumerate(self.modelo[1:]):
            if estado == "sucio":
                objetivo = i
                break
        
        # trate de mejorar la lógica del agente reactivo modelo anterior, 
        # calculando depende del piso en el que esta. Al final hacen lo
        # mismo.
        if objetivo is not None:
            piso_robot = robot // 3  
            piso_objetivo = objetivo // 3
            
            if piso_robot == piso_objetivo:
                if objetivo > robot:
                    return "ir_Derecha"
                else:
                    return "ir_Izquierda"
            
            elif piso_objetivo > piso_robot:
                if robot not in (2, 5):
                    return "ir_Derecha"
                else:
                    return "subir"
            
            else:
                if robot not in (3, 6):
                    return "ir_Izquierda"
                else:
                    return "bajar"

        return "nada"

def test():
    x0 = [0, "sucio", "sucio", "sucio", 
             "sucio", "sucio", "sucio", 
             "sucio", "sucio", "sucio",]
    
    """
    OBSERVACIONES 
    No me quedo claro si tenia que comparar los agentes de cada entorno con el aleatorio normal, 
    o con uno aleatorio para cada entorno, por lo cual compare cada uno con un agente
    aleatorio en ese mismo entorno.

    Reduje el numero de iteraciones para los agentes racionales ya que solo les tomaba alrededor
    de 30 iteraciones limpiar todos los cuartos, y hacia mucho clutter en el output.

    """

    # Primer y segundo punto de la tarea
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteAleatorioNueveCuartos(),
                         200)
    
    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteReactivoModeloNueveCuartos(),
                         50)
    
    # Tercer punto de la tarea 
    print("Prueba del entorno ciego con un agente aleatorio")
    entornos_o.simulador(NueveCuartosCiego(x0),
                         AgenteAleatorioNueveCuartosCiego(),
                         200)
    
    print("Prueba del entorno ciego con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosCiego(x0),
                         AgenteReactivoModeloNueveCuartosCiego(),
                         50)
    
    # Cuarto punto de la tarea
    print("Prueba del entorno estocástico con un agente aleatorio")
    entornos_o.simulador(NueveCuartosEstocastico(x0),
                         AgenteAleatorioNueveCuartos(),
                         200)
    
    print("Prueba del entorno estocastico con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosEstocastico(x0),
                         AgenteReactivoModeloNueveCuartosEstocastico(),
                         50)
    
if __name__ == "__main__":
    test()