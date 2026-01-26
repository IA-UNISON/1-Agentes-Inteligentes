#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Melina González Méndez'

import entornos_f
import entornos_o

#NueveCuartos
class NueveCuartos():
     """
     Clase para un entorno de nueve cuartos (3 pisos x 3 cuartos). 
     
                  [G   H   I    Piso 3
     Cuartos =     D   E   F    Piso 2
                   A   B   C]   Piso 1

     El estado se define como (robot, cuartos)
     donde el robot puede estar en cualquier cuarto. Cada cuarto tiene los valores "limpio" o "sucio".

     Acciones: ["ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada"]

     Costos: Cada accion tiene un costo asociado.
             0 si todos los cuartos están limpios y la acción es nada.
             3 si la acción es subir o bajar.
             1 para cualquier otra acción.
             Si la accion no es legal, el estado no cambia y el costo es 0.
     """
     #Reglas:
     cuartos = ("A","B","C","D","E","F","G","H","I")
     derecha = {"A":"B", "B":"C", "D":"E", "E":"F", "G":"H", "H":"I"}
     izquierda = {"C":"B", "B":"A", "F":"E", "E":"D", "I":"H", "H":"G"}
     subir = {"C":"F", "F":"I"}
     bajar = {"G":"D", "D":"A"}

     def accion_legal(self, estado, accion):
        """
       Revisa si la acción es legal. Para ello debe de cumplir con las siguientes reglas:
        ir_Derecha: A -> B, B -> C, D->E, E->F, G->H, H->I
 	    ir_Izquierda: C-> B, B-> A, F-> E, E->D, I->H, H -> G
        subir: C->F, F->I (solo legal en los primeros dos pisos, en los cuartos de la derecha).
	    bajar: G->D, D->A (solo legal en los dos pisos de arriba, en los cuartos de la izquierda).
        limpiar: Cambia el estado del cuarto actual a limpio.
        Nada: La accion no hace ningún cambio en el entorno.

        """
        robot, _ = estado

        if accion == "ir_derecha":
            return robot in self.derecha
        if accion == "ir_izquierda":
            return robot in self.izquierda
        if accion == "subir":
            return robot in self.subir
        if accion == "bajar":
            return robot in self.bajar
        if accion in ("limpiar", "nada"):
            return True
        return False
     
     def transicion(self, estado, accion):
         """
         Aplica la acción al estado. Si la acción no es legal, el estado se queda igual.
         """
         robot, cuartos = estado

         cuartos_nuevo = dict(cuartos)

         #Comprobar si estan limpio todos los cuartos
         todolimpio = True
         for q in self.cuartos:
             if cuartos_nuevo[q] != "limpio":
                 todolimpio = False
                 break
         
         #Costo
         c_local = (0 if (todolimpio and accion == "nada") else
                    3 if accion in ("subir", "bajar") else 1)
         
         if not self.accion_legal(estado, accion):
             return (robot, cuartos_nuevo), 0
         if accion == "ir_derecha":
             robot = self.derecha[robot]
         elif accion == "ir_izquierda":
             robot = self.izquierda[robot]
         elif accion == "subir":
             robot = self.subir[robot]
         elif accion == "bajar":
             robot = self.bajar[robot]
         elif accion == "limpiar":
             cuartos_nuevo[robot] = "limpio"
         elif accion == "nada":
             pass
         
         return (robot, cuartos_nuevo), c_local

     def percepcion(self, estado):
         """
         Muestra donde está el robot y si el cuarto actual esta limpio o sucio.
         """
         robot, cuartos = estado
         return (robot, cuartos[robot])

