#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 26/04/2014

@author: daniel
@contact: cdaniel.py@gmail.com
@summary: prueba de modulos y clases de uniones

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

    oConexion._bMostrarSql = True

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
 
    #restricciones sobre cadenas
    cSentencia = emp.filtrar(Restriccion.Como(cApellido = '%Piveteau%'))

    #ejecutamos la consulta
    lResultado = oConexion.lEjecutarConsulta(cSentencia)

    if lResultado[0] != 1: raise Exception(lResultado[1])

    lCampos = Employee()._dicCampos.keys()

    #recorremos las filas devueltas, instanciamos la clase correspondiente
    #e imprimimos su representacion
    for fila in lResultado[1]: print Employee(**dict(zip(lCampos, fila)))
