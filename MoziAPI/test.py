#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 13/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: prueba de modulos y clases

    Utilizamos una conexion a una BD mysql/mariadb y la base de datos de ejemplo
    EMPLOYEES, que se puede descargar en el siguiente enlace http://launchpad.net/test-db/

'''


#importamos los modulos y clases necesarias
from testing.mysqlutiles import MySqlUtiles
from testing.otds import Employee, Department, DepEmp
from org.moziapi.restricciones import Restriccion
from datetime import datetime
from org.moziapi.uniones.union import Union



if __name__ == '__main__':

    # iniciamos la conexion a la BD
    oConexion = MySqlUtiles('localhost', '', 'employees', 'root', 'password')

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
#    cSentencia = Employee().filtrar(Restriccion.O(
#                                                  [
#                                                  Restriccion.Ig(_nId = '10008')
#                                                  ,Restriccion.Y([
#                                                                 Restriccion.Ig(_nId = 100011)
#                                                                , Restriccion.Ig(_dFechaIngreso = datetime(1985, 1, 1))
#                                                                 ])
#                                                  ]
#                                                  )
#                                             )


#################################################

#             UNIENDO TABLAS

#################################################

    emp = Employee(cAlias = '_emp_')
    emp.unir(Union.Normal(_dep_ = DepEmp))

    #si obviamos la restriccion se convierte en un crossjoin

    #join via sql nativo
#     cSentencia = emp.filtrar('_dep_.emp_no = _emp_.emp_no')
#    cSentencia = emp.filtrar('_dep_.emp_no = _emp_.emp_no AND _emp_.id BETWEEN 10008 AND 10015') 

    #join via Restriccion
#    cSentencia = emp.filtrar(Restriccion.Ig('_emp_.emp_no', '_dep_.emp_no'))
#     cSentencia = emp.filtrar(Restriccion.Y([
#                                               Restriccion.Ig('_emp_.emp_no', '_dep_.emp_no')
#                                               , Restriccion.Entre(_nId=[10008, 10050])
#                                               , Restriccion.Dif('_emp_.emp_no', '10011')
#                                               , Restriccion.MenIg(_nId = 10034)
#                                               , Restriccion.May(_nId = 10009)
#                                               ]
#                                ))

    #restricciones sobre cadenas
#     cSentencia = emp.filtrar(Restriccion.Como('_emp_.last_name', '%Piveteau%'))
    cSentencia = emp.filtrar(Restriccion.Como(_cApellido = '%Piveteau%'))

#################################################
#################################################

    lResultado = oConexion.lEjecutarConsulta(cSentencia)
    if lResultado[0] != 1: raise Exception(lResultado[1])

    n = 0
    lCampos = Employee()._dicCampos.keys()

    for fila in lResultado[1]:
        print fila
        emp = Employee(**dict(zip(lCampos, fila)))
        print emp

        n += 1
        if n > 50: break

