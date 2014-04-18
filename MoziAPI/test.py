#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: prueba de modulos y clases

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

    #preguntamos por la contrasena de acceso a la base de datos
    pwd = raw_input('contrasena MySQL: ')

    #instanciamos la utileria
    oConexion = MySqlUtiles('localhost', '', 'employees', 'root', pwd)

    # iniciamos la conexion a la BD
    lResultado = oConexion.lConectar()

    # si no se conecto
    if lResultado[0] != 1: raise Exception(lResultado[1])

    oConexion._bMostrarSql = True

    # una consulta basica
    #cSentencia = Employee().select

    #filtro simple
    #cSentencia = Employee().filtrar(Restriccion.Ig(_nId = 10008))

    #filtro por rango de valores
    #cSentencia = Employee().filtrar(Restriccion.Entre(_nId=[10008, 10015]))

    #filtro OR con AND
#===============================================================================
#     oRest_Y = Restriccion.Y((
#                          Restriccion.Ig(_nId = 100011)
#                         , Restriccion.Ig(dFechaIngreso = datetime(1985, 1, 1))
#                          ))
# 
#     oRest_O = Restriccion.O((Restriccion.Ig(_nId = '10008')
#                           , oRest_Y
#                           ))
# 
#     #obtenemos la sentecia formada
#     cSentencia = Employee().filtrar(oRest_O)
#===============================================================================


#################################################

#             UNIENDO TABLAS

#################################################

    #una instancia de la clase Employee con un alias para su tabla
    emp = Employee(cAlias = '_emp_')
 
    #join con la tabla [dept_emp]
    emp.unir(Union(_de_ = DeptEmp
                   , cTipo = Union.NORMAL
                   #las resctricciones de uniones deben crearse por cadenas
                   # no por atributos
                   , oRestriccion = Restriccion.Ig('_emp_.emp_no'
                                                   , '_de_.emp_no'
                                                   )
                   )
             )
 
    #join con la tabla [departments]
    emp.unir(Union(_dep_ = Department
                   , cTipo = Union.NORMAL
                   , oRestriccion = Restriccion.Ig('_de_.dept_no'
                                                   , '_dep_.dept_no'
                                                   )
                   )
             )
 
    #restricciones via sql nativo
    #===========================================================================
    # cSentencia = emp.filtrar('_de_.emp_no <= 10034'
    #                          + ' AND _emp_.emp_no BETWEEN 10008 AND 10015'
    #                          ) 
    #===========================================================================

    #restricciones sobre cadenas
    cSentencia = emp.filtrar(Restriccion.Como(cApellido = '%Piveteau%'))

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

#################################################
#################################################

    lResultado = oConexion.lEjecutarConsulta(cSentencia)
    if lResultado[0] != 1: raise Exception(lResultado[1])

    n = 0
    lCampos = Employee()._dicCampos.keys()

    for fila in lResultado[1]:
        #print fila
        emp = Employee(**dict(zip(lCampos, fila)))
        print emp.cDescripcion

        n += 1
        if n > 50: break

    print 'moziapi.__VERSION__ =', moziapi.__VERSION__