#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: prueba de modulos y clases de seleccion con union de dependencias

    Utilizamos una conexion a una BD mysql/mariadb y la base de datos
    de ejemplo EMPLOYEES, que se puede descargar en el siguiente enlace
    
    http://launchpad.net/test-db/

'''


#importamos los modulos y clases necesarias
from testing.mysqlutiles import MySqlUtiles
from testing.otds import Employee, Department, DeptEmp
from datetime import datetime
from moziapi import Union, Restriccion
import moziapi



if __name__ == '__main__':

    print 'moziapi.__VERSION__ =', moziapi.__VERSION__
    print ''

    #preguntamos por la contrasena de acceso a la base de datos
    pwd = raw_input('contrasena MySQL: ')

    #instanciamos la utileria
    oConexion = MySqlUtiles('localhost', '', 'employees', 'root', pwd)

    # iniciamos la conexion a la BD
    lResultado = oConexion.lConectar()

    # si no se conecto
    if lResultado[0] != 1: raise Exception(lResultado[1])

    oConexion.mostrarSQL(True)

########################################################################
#   EJECUCION DIRECTA, RECUPERACION DE TUPLAS Y CREACION DE INSTANCIAS
########################################################################

    # una consulta basica (OJO, sin limites, no se recomienda su uso)
    #cSentencia = Employee().select

    #filtro simple
    #cSentencia = Employee().filtrar(Restriccion.Ig(nId = 10008))

    #restricciones via sql nativo
    #===========================================================================
    # cSentencia = emp.filtrar(emp_no BETWEEN 10008 AND 10015') 
    #===========================================================================

    #restricciones multiples (AND)
#===============================================================================
#     oRest_Y = Restriccion.Y(
#                         (Restriccion.Ig('_de_.dept_no', "'d004'")
#                          , Restriccion.Ig('_de_.to_date'
#                                           , datetime(9999, 1, 1)
#                                           )
#                          )
#                         )
# 
#     #obtenemos la sentencia formada
#     cSentencia = emp.filtrar(oRest_Y)
#===============================================================================


    #filtro por rango de valores
    cSentencia = Employee().filtrar(Restriccion.Entre(nId=[10008, 10015]))

    #ejecutamos la consulta
    lResultado = oConexion.lEjecutarConsulta(cSentencia)
 
    if lResultado[0] != 1: raise Exception(lResultado[1])
 
    #recuperamos los campos de la clase
    lCampos = Employee()._dicCampos.keys()
 
    #recorremos las filas devueltas, instanciamos la clase correspondiente
    #e imprimimos su representacion
    print type(lResultado[1])
    for fila in lResultado[1]: print Employee(**dict(zip(lCampos, fila)))



########################################################################
#   EJECUCION INDIRECTA, RECUPERACION DE INSTANCIAS
########################################################################

#===============================================================================
#     #ejecutamos la recuperacion de instancias a traves de un generador
#     gen = oConexion.gRecuperar(Employee, Restriccion.Entre(nId=[10070, 10090]))
# 
#     #recorremos el generador e imprimimos su representacion
#     for emp in gen:
#         print emp           #la instancia en si
#         #listamos el historial de departammentos del empleado
#         for deptEmp in emp.DeptEmps:
#             print deptEmp,
#             print deptEmp.Department #los datos del Departamento
#===============================================================================


