#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'alejandro_barreras'

import entornos_f
import entornos_o

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python



######################################################################################



# 1) Nueve Cuartos


from random import choice

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de 9 cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, piso, A1, B1, C1, A2, B2, C2, A3, B3, C3)
    donde robot puede tener los valores "A", "B", "C"
    piso puede tener los valores 1, 2, 3
    A1, B1, C1, A2, B2, C2, A3, B3, C3 pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_Izquierda", 
    "ir_Derecha", "subir", "bajar", "limpiar", "nada").
    No todas las acciones son válidas en todos los estados.

    La acción "subir" solo es legal en los primeros dos pisos y cuando el
    robot está en el cuarto C. La acción "bajar" solo es legal en los
    segundos y terceros pisos y cuando el robot está en el cuarto A.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", 1, 
                           "sucio", "sucio", "sucio",
                           "sucio", "sucio", "sucio",
                           "sucio", "sucio", "sucio"]):
        
        """

        Por default inicialmente el robot está en el cuarto A, en el primer piso
        y todos los cuartos están sucios

        """
        self.x = x0[:]
        self.costo = 0
    
    def indice_cuarto(self, piso, cuarto):
        return 2 + (piso - 1) * 3 + "ABC".find(cuarto)

    def accion_legal(self, accion):
        robot = self.x[0] 
        piso = self.x[1]

        if accion in ("limpiar", "nada"):
            return True
        if accion == "ir_Izquierda":
            return robot != "A"
        if accion == "ir_Derecha":
            return robot != "C"
        if accion == "subir":
            return piso < 3 and robot == "C"
        if accion == "bajar":
            return piso > 1 and robot == "A"
        
        return False

    def transicion(self, accion):
        robot = self.x[0]
        piso = self.x[1]
        
        if not self.accion_legal(accion):
            self.costo += 5
            return
        
        if accion == "limpiar":
            self.costo += 1
        elif accion == "ir_Izquierda":
            self.costo += 2
        elif accion == "ir_Derecha":
            self.costo += 2
        elif accion == "subir":
            self.costo += 3
        elif accion == "bajar":
            self.costo += 3

        if accion == "limpiar":
            i = self.indice_cuarto(piso, robot)
            self.x[i] = "limpio"
        elif accion == "ir_Izquierda":
            self.x[0] = "ABC"[ "ABC".find(robot) - 1 ]
        elif accion == "ir_Derecha":
            self.x[0] = "ABC"[ "ABC".find(robot) + 1 ]
        elif accion == "subir":
            self.x[1] += 1
        elif accion == "bajar":
            self.x[1] -= 1

    def percepcion(self):
        robot = self.x[0]
        piso = self.x[1]
        situacion = self.x[self.indice_cuarto(piso, robot)]
        return robot, piso, situacion



######################################################################################



# 2) Agentes reactivos y agente aleatorio


class AgenteReactivoNuevecuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepcion):
        robot, piso, situacion = percepcion
        if situacion == 'sucio':
            return 'limpiar'
        elif robot == 'A' and piso > 1:
            return 'bajar'
        elif robot == 'C' and piso < 3:
            return 'subir'
        elif robot != 'C':
            return 'ir_Derecha'
        else:
            return 'ir_Izquierda'


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 1,
                       'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio',
                       'sucio', 'sucio', 'sucio']
    
    def indice_cuarto(self, piso, cuarto):
        return 2 + (piso - 1) * 3 + "ABC".find(cuarto)

    def programa(self, percepcion):
        robot, piso, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[1] = piso
        self.modelo[self.indice_cuarto(piso, robot)] = situacion

        # Decide sobre el modelo interno
        return (
            'nada' if 'sucio' not in self.modelo[2:] else
            'limpiar' if situacion == 'sucio' else
            'ir_Izquierda' if robot != 'A' and 'sucio' in self.modelo[self.indice_cuarto(piso, 'A'):
                                                                      self.indice_cuarto(piso, robot)] else
            'ir_Derecha' if robot != 'C' else
            'subir' if piso < 3 else 
            'nada'
            )
    
    """

    Obervaciones al comparar con agente aleatorio:

    - El agente aleatorio tarda más en limpiar todos los cuartos, además de que
      gasta más recursos (costo mayor). Y no garantiza que limpie todos los cuartos
      en un número fijo de pasos.

    - El agente reactivo basado en modelo garantiza que limpiará todos los cuartos en
      una cantidad pasos determinados, ya que cuando llega a un cuarto checa si está 
      sucio y lo limpia, y si está limpio se mueve al siguiente cuarto sistemáticamente. 
      Así que su costo es menor.

    """



######################################################################################



# 3)


class NueveCuartosCiego(NueveCuartos):
    """
    Igual que DosCuartos, pero no se puede ver nada

    """
    def percepcion(self):
        robot = self.x[0]
        piso = self.x[1]

        return robot, piso, '?'


class AgenteReactivoModeloNueveCuartosCiego(entornos_o.Agente):
    """
    Agente reactivo basado en modelo.

    """
    
    def __init__(self):
        self.modelo = ['?', '?',
                       'no_visitado', 'no_visitado', 'no_visitado',
                       'no_visitado', 'no_visitado', 'no_visitado',
                       'no_visitado', 'no_visitado', 'no_visitado']
    
    def indice_cuarto(self, piso, cuarto):
        return 2 + (piso - 1) * 3 + "ABC".find(cuarto)
    
    def programa(self, percepcion):
        robot, piso, _ = percepcion
        
        self.modelo[0] = robot
        self.modelo[1] = piso
        
        indice_actual = self.indice_cuarto(piso, robot)

        # Si ya se visitaron todos los cuartos, hacer nada
        if 'no_visitado' not in self.modelo[2:]:
            return 'nada'
        # Si el cuarto actual no ha sido visitado, limpiarlo
        if self.modelo[indice_actual] == 'no_visitado':
            self.modelo[indice_actual] = 'visitado'
            return 'limpiar'
        
        # Revisar cuartos actuales
        a_actual = self.indice_cuarto(piso, 'A')
        b_actual = self.indice_cuarto(piso, 'B')
        c_actual = self.indice_cuarto(piso, 'C')
        
        if (self.modelo[a_actual] == 'no_visitado' or 
            self.modelo[b_actual] == 'no_visitado' or 
            self.modelo[c_actual] == 'no_visitado'):
            
            if robot == 'A':
                return 'ir_Derecha'
            elif robot == 'B':
                if self.modelo[c_actual] == 'no_visitado':
                    return 'ir_Derecha'
                else:
                    return 'ir_Izquierda'
            else:  
                return 'ir_Izquierda'

        # Revisar los pisos 2 y 3
        if piso == 1:
            a2 = self.indice_cuarto(2, 'A')
            b2 = self.indice_cuarto(2, 'B')
            c2 = self.indice_cuarto(2, 'C')
            if (self.modelo[a2] == 'no_visitado' or 
                self.modelo[b2] == 'no_visitado' or 
                self.modelo[c2] == 'no_visitado'):
                if robot != 'C':
                    return 'ir_Derecha'
                else:
                    return 'subir'

            a3 = self.indice_cuarto(3, 'A')
            b3 = self.indice_cuarto(3, 'B')
            c3 = self.indice_cuarto(3, 'C')
            if (self.modelo[a3] == 'no_visitado' or 
                self.modelo[b3] == 'no_visitado' or 
                self.modelo[c3] == 'no_visitado'):
                if robot != 'C':
                    return 'ir_Derecha'
                else:
                    return 'subir'
        
        # Revisar los pisos 1 y 3
        elif piso == 2:
            a3 = self.indice_cuarto(3, 'A')
            b3 = self.indice_cuarto(3, 'B')
            c3 = self.indice_cuarto(3, 'C')
            if (self.modelo[a3] == 'no_visitado' or 
                self.modelo[b3] == 'no_visitado' or 
                self.modelo[c3] == 'no_visitado'):
                if robot != 'C':
                    return 'ir_Derecha'
                else:
                    return 'subir'
            
            a1 = self.indice_cuarto(1, 'A')
            b1 = self.indice_cuarto(1, 'B')
            c1 = self.indice_cuarto(1, 'C')
            if (self.modelo[a1] == 'no_visitado' or 
                self.modelo[b1] == 'no_visitado' or 
                self.modelo[c1] == 'no_visitado'):
                if robot != 'A':
                    return 'ir_Izquierda'
                else:
                    return 'bajar'
        
        # Revisar los pisos 1 y 2
        elif piso == 3:
            a2 = self.indice_cuarto(2, 'A')
            b2 = self.indice_cuarto(2, 'B')
            c2 = self.indice_cuarto(2, 'C')
            if (self.modelo[a2] == 'no_visitado' or 
                self.modelo[b2] == 'no_visitado' or 
                self.modelo[c2] == 'no_visitado'):
                if robot != 'A':
                    return 'ir_Izquierda'
                else:
                    return 'bajar'
            
            a1 = self.indice_cuarto(1, 'A')
            b1 = self.indice_cuarto(1, 'B')
            c1 = self.indice_cuarto(1, 'C')
            if (self.modelo[a1] == 'no_visitado' or 
                self.modelo[b1] == 'no_visitado' or 
                self.modelo[c1] == 'no_visitado'):
                if robot != 'A':
                    return 'ir_Izquierda'
                else:
                    return 'bajar'
        
        return 'nada'
    
    """

    Observaciones al comparar con agente aleatorio:

    - El agente aleatorio tarda más en limpiar todos los cuartos, además de que
      gasta más recursos (costo mayor). Y no garantiza que limpie todos los cuartos
      en un número fijo de pasos.

    - El agente racional ciego garantiza que limpiará todos los cuartos en un tiempo
      determinado ya que cada cuarto que visita lo limpia, y mantiene un registro 
      de los cuartos visitados para no regresar a ellos innecesariamente. Así que es
      más eficiente que el agente aleatorio.

    """


######################################################################################



# 4)

class NueveCuartosEstocástico(NueveCuartos):
    """
    Igual que NueveCuartos, pero... 
    - limpiar funciona el 80% de las veces y el 20% falla y deja sucio el cuarto.
    - Las acciones de movimiento funcionan el 80% de las veces, el 10% no hacen 
      nada y el otro 10% hacen una acción al azar.

    """
    def transicion(self, accion):
        from random import random
        from random import choice

        rand = random()

        if accion == "limpiar":
            if rand < 0.8:
                super().transicion(accion)
                return
            else:
                self.costo += 1
                return
        elif accion in ("ir_Izquierda", "ir_Derecha", "subir", "bajar", "nada"):
            if rand < 0.8:
                NueveCuartos.transicion(self, accion)
            elif rand < 0.9:
                self.costo += 1
            else:
                acciones_legales = [a for a in ("ir_Izquierda", "ir_Derecha", "subir", "bajar", "limpiar", "nada")
                                    if self.accion_legal(a) and a != accion]
                accion_azar = choice(acciones_legales)
                NueveCuartos.transicion(self, accion_azar)
        else:
            NueveCuartos.transicion(self, accion)
    
    """

    Observaciones al comparar con agente aleatorio:

    - El agente aleatorio tarda más en limpiar todos los cuartos, además de que
      gasta más recursos (costo mayor). Y no garantiza que limpie todos los cuartos
      en un número fijo de pasos.

    - El agente estocástico revisa y limpia cada cuarto sistemáticamente, aunque 
      algunas veces falle al limpiar o al moverse, eventualmente limpiará todos 
      los cuartos en un tiempo determinado. Así que su costo es menor que el agente 
      aleatorio.

    """
        

######################################################################################

# Pruebas:

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)

def test():
    """
    Prueba del entorno y los agentes

    """
    x0=["A", 1,
         "sucio", "sucio", "sucio",
         "sucio", "sucio", "sucio",
         "sucio", "sucio", "sucio"]
    
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir',
                                          'bajar', 'limpiar', 'nada']),
                         200)

    #print("Prueba del entorno con un agente reactivo")
    #entornos_o.simulador(NueveCuartos(x0), 
    #                    AgenteReactivoNuevecuartos(), 
    #                     200)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(x0), 
                         AgenteReactivoModeloNueveCuartos(), 
                         200)

    print("Prueba del entorno ciego con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosCiego(x0), 
                         AgenteReactivoModeloNueveCuartosCiego(), 
                         200)
    
    print("Prueba del entorno estocástico con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartosEstocástico(x0), 
                         AgenteReactivoModeloNueveCuartos(), 
                         200)

if __name__ == "__main__":
    test()
